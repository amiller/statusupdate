<?php

/* Servers configuration */
$i = 0;

$i++;
$cfg['Servers'][$i]['host'] = 'localhost';
$cfg['Servers'][$i]['extension'] = 'mysqli';
$cfg['Servers'][$i]['connect_type'] = 'tcp';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['auth_type'] = 'config';
$cfg['Servers'][$i]['user'] = '{DBUSER}';
$cfg['Servers'][$i]['password'] = '{PASSWORD}';
$cfg['Servers'][$i]['only_db'] = '{DATABASE}';

$cfg['Servers'][$i]['AllowDeny']['order'] = '';

$cfg['Servers'][$i]['AllowDeny']['rules'] = array();


/* End of servers configuration */

?>
