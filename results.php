<?php

ini_set('auto_detect_line_endings', true);

$cache_dir = './cache/';

function throw_error($msg) {
    die(json_encode(array('error' => true, 'reason' => $msg)));
}

function debug($msg) {
    if ( isset($_SERVER['argc']) )
        echo "$msg\n";
}

if ( isset($_GET['id']) )
    $electorate_id = $_GET['id'];
else if ( isset($_SERVER['argc']) && $_SERVER['argc'] > 1 )
    $electorate_id = $_SERVER['argv'][1];
else
    throw_error("No electorate ID");

if ( !is_numeric($electorate_id) )
    throw_error("Invalid electorate ID");

if ( file_exists($cache_dir . $electorate_id . '.js') && !isset($_GET['refresh']) ) {
    $res = unserialize(file_get_contents($cache_dir . $electorate_id . '.js'));
    die(json_encode(array('error' => false, 'polling_places' => $res)));
}

$polling_places = array();

/* Load list of polling places */

debug("Loading polling places.");

$dom = new DOMDocument();
if ( !$dom->loadHTMLFile('http://results.aec.gov.au/15508/Website/HouseDivisionPollingPlaces-15508-' . $electorate_id . '.htm') )
    throw_error("Couldn't load polling place list.");

$x = new DOMXPath($dom);
$rows = $x->query("//tr[@class='rownorm']");

foreach ( $rows as $row ) {
    $subDom = new DOMDocument();
    $subDom->appendChild($subDom->importNode($row, true));
    $sx = new DOMXPath($subDom);
    
    $link = $sx->query("//a");
    if ( $link->length != 1 )
        continue;
    
    $url = $link->item(0)->attributes->getNamedItem('href')->nodeValue;
    $id = str_replace(array('HousePollingPlaceFirstPrefs-15508-', '.htm'), '', $url);
    if ( $id == '' )
        continue;

    $name = $link->item(0)->nodeValue;
    if ( stripos($name, "Special Hospital Team") !== FALSE )
        continue;
    
    $tds = $sx->query("//td");
    if ( $tds->length != 2 )
        continue;
    
    $address = $tds->item(1)->nodeValue;
    
    $polling_places[$id] = array(
        'name' => $name,
        'address' => $address
    );
    
    
    
    debug("\t$name");
}

/* Geocode the addresses */

debug("Geocoding addresses.");

foreach ( $polling_places as $id => $details ) {
    debug("\t{$details['name']}");
    $json = file_get_contents('http://maps.googleapis.com/maps/api/geocode/json?address=' . urlencode($details['address']) . '&sensor=false');
    if ( $json ) {
        $geo = json_decode($json, true);
        if ( $geo['status'] == "OK" ) {
            if ( isset($geo['results'][0]['geometry']['location']) ) {
                $polling_places[$id]['loc'] = array(
                    'lat' => $geo['results'][0]['geometry']['location']['lat'],
                    'lng' => $geo['results'][0]['geometry']['location']['lng']
                );
                debug("\t\tLocation found");
            }
        }
    }
}

/* Get results for each polling place */

debug("Loading results.");

$r = fopen('./HouseTppByPollingPlaceDownload-15508.csv', 'r');
if ( !$r ) throw_error("Results file error");

$results = array();

while ( !feof($r) ) {
    $row = fgetcsv($r);
    if ( count($row) < 9 ) continue;
    if ( $row[1] == $electorate_id ) {
        $results[$row[3]] = array(
            'alp' => $row[6],
            'lnp' => $row[8],
            'tot' => $row[9] - ($row[9] % 100)
        );
    }
}

foreach ( $polling_places as $id => $details ) {
    if ( isset($results[$id]) )
        $polling_places[$id]['2pp'] = $results[$id];
}

/* Transform to a normal array */
$res = array();
foreach ( $polling_places as $id => $details ) {
    $details['id'] = $id;
    $res[] = $details;
}

file_put_contents($cache_dir . $electorate_id . '.js', serialize($res));
echo json_encode(array('error' => false, 'polling_places' => $res));

?>