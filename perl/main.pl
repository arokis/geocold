 #!/usr/bin/perl
 use LWP::Simple;
 use RDF::Simple::Parser;

 
 my $id = 'http://sws.geonames.org/2813436/about.rdf';
 $contents = get($id);
 print $contents;