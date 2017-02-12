<?php
/////////////////
// Basic Parse :
/* 
    Extract text from elements
        - (Not Basic Enough) only choose text which has more than 5 words around it (removes headers, bullet points, simple things around it. ????? )
        - (Not implemented on purpose) throwout meta, throwout scripts
        
   Normalize:
        - Lowercase everything
        - remove numbers                    (?) -vs- replace with NUM (-------------------- optimization)
        - multiple whitespace = one whitespace
        -  remove ALL nonalpha characters   (?) -vs- remove all nonalpha characters except "'", and ".", (----------- optiization)
   Tokenize: 
        - Split words into an array/list
            - e.g., "the", "sly", "fox", "jumped", "over", ...
            
   Cont Normalize:
        - remove stopwords  (MYSQL STOP WORDS)
*/


function normalizationPartOne($content){
    //used because stopwords needs same normalization
 
    $content = preg_replace("/[\r\n]+/", " ", $content); // replace new lines with spaces
    $content = strtolower($content); // lowercase everything
    $content = preg_replace('/[0-9]+/', '', $content); // remove all numbers
    $content = preg_replace('/\s+/', ' ', $content); // replace multiple white spaces with one white space
    $content = preg_replace("/[^A-Za-z ]/", '', $content); // remove all nonalpha characters 

    
    
    return $content;
}

function DOMinnerHTML(DOMNode $element) { 
    $innerHTML = ""; 
    $children  = $element->childNodes;

    foreach ($children as $child) 
    { 
        $innerHTML .= $element->ownerDocument->saveHTML($child);
    }

    return $innerHTML; 
} 



function parseThisURL($html, $stop_boolean){
    //var_dump($html);
    $stopWords = $GLOBALS["stopWords"];
    if($dontUse_stopWords_boolean == true){
        $stopWords = [];   
    }
    
    /////////////////////////////
    // Get text from document (very naieve approach)
    //   + remove scripts
    //////
    $dom = new DOMDocument();
    $dom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8')); // This way we dont get funny letters
    $dom->strictErrorChecking = false;
    $dom->formatOutput = true;
    // remove scripts and styles
    while (($r = $dom->getElementsByTagName("script")) && $r->length) {
            $r->item(0)->parentNode->removeChild($r->item(0));
    }
    while (($r = $dom->getElementsByTagName("style")) && $r->length) {
            $r->item(0)->parentNode->removeChild($r->item(0));
    }
    
    // get content in plain text format
    //$content = $dom->textContent; - deprecated 1/18/17 
    $content = $dom->saveHTML();
    $content = strip_tags($content); // remove html tags
    $content = html_entity_decode($content); // Clean up things like &amp;
    $content = urldecode($content); // Strip out any url-encoded stuff
    //var_dump($html);
    var_dump($content);

    /////////////////////////////
    // Normalize Part One
    ////
    $content = normalizationPartOne($content);
    //var_dump($content);
    
    //////////////////////////////
    // Tokenize
    ////
    $content = explode(" ", $content);
    
    //////////////////////////////
    // Normalize part 2 (token based)
    ////
    $old_content = $content;
    $content = [];
    for($index = 0; $index < count($old_content); $index++){
        $thisWord = $old_content[$index];
        
        /*
        $booleans = [
            strlen($thisWord) > 2, // make sure word is more than 2 char long
            strlen($thisWord) < 30, // make sure word is less than 30 char long
            !in_array($thisWord, $stopWords), // remove all stop words
        ];
        
        
        $fails_booleans = false;
        for($i = 0; $i < count($booleans); $i++){
            $thisBoolean = $booleans[$i];
            if(!$thisBoolean){
                $fails_booleans = true;
                break;
            }
        }
        */
        
        
        $fails_booleans = false;
        if(strlen($thisWord) < 2 || in_array($thisWord, $stopWords)){
            $fails_booleans = true;   
        }
        
        if($index !== 0 && $thisWord == $lastWord){ 
            // Eliminate Repetitions - removes problems with web data where strings like, sih sih sih sih sih sih sih sih, make everything close to sih
            $fails_booleans = true;
        }
        $lastWord = $thisWord;
        
        
        if(!$fails_booleans){
            $content[] = $thisWord;   
        }
    }
    //var_dump(implode(" ", $content));

    return $content;
}
   

$GLOBALS["stopWords"] = [];
//http://www.ranks.nl/stopwords --- MYSQL LIST USED
$list = "
a's	able	about	above	according
accordingly	across	actually	after	afterwards
again	against	ain't	all	allow
allows	almost	alone	along	already
also	although	always	am	among
amongst	an	and	another	any
anybody	anyhow	anyone	anything	anyway
anyways	anywhere	apart	appear	appreciate
appropriate	are	aren't	around	as
aside	ask	asking	associated	at
available	away	awfully	be	became
because	become	becomes	becoming	been
before	beforehand	behind	being	believe
below	beside	besides	best	better
between	beyond	both	brief	but
by	c'mon	c's	came	can
can't	cannot	cant	cause	causes
certain	certainly	changes	clearly	co
com	come	comes	concerning	consequently
consider	considering	contain	containing	contains
corresponding	could	couldn't	course	currently
definitely	described	despite	did	didn't
different	do	does	doesn't	doing
don't	done	down	downwards	during
each	edu	eg	eight	either
else	elsewhere	enough	entirely	especially
et	etc	even	ever	every
everybody	everyone	everything	everywhere	ex
exactly	example	except	far	few
fifth	first	five	followed	following
follows	for	former	formerly	forth
four	from	further	furthermore	get
gets	getting	given	gives	go
goes	going	gone	got	gotten
greetings	had	hadn't	happens	hardly
has	hasn't	have	haven't	having
he	he's	hello	help	hence
her	here	here's	hereafter	hereby
herein	hereupon	hers	herself	hi
him	himself	his	hither	hopefully
how	howbeit	however	i'd	i'll
i'm	i've	ie	if	ignored
immediate	in	inasmuch	inc	indeed
indicate	indicated	indicates	inner	insofar
instead	into	inward	is	isn't
it	it'd	it'll	it's	its
itself	just	keep	keeps	kept
know	known	knows	last	lately
later	latter	latterly	least	less
lest	let	let's	like	liked
likely	little	look	looking	looks
ltd	mainly	many	may	maybe
me	mean	meanwhile	merely	might
more	moreover	most	mostly	much
must	my	myself	name	namely
nd	near	nearly	necessary	need
needs	neither	never	nevertheless	new
next	nine	no	nobody	non
none	noone	nor	normally	not
nothing	novel	now	nowhere	obviously
of	off	often	oh	ok
okay	old	on	once	one
ones	only	onto	or	other
others	otherwise	ought	our	ours
ourselves	out	outside	over	overall
own	particular	particularly	per	perhaps
placed	please	plus	possible	presumably
probably	provides	que	quite	qv
rather	rd	re	really	reasonably
regarding	regardless	regards	relatively	respectively
right	said	same	saw	say
saying	says	second	secondly	see
seeing	seem	seemed	seeming	seems
seen	self	selves	sensible	sent
serious	seriously	seven	several	shall
she	should	shouldn't	since	six
so	some	somebody	somehow	someone
something	sometime	sometimes	somewhat	somewhere
soon	sorry	specified	specify	specifying
still	sub	such	sup	sure
t's	take	taken	tell	tends
th	than	thank	thanks	thanx
that	that's	thats	the	their
theirs	them	themselves	then	thence
there	there's	thereafter	thereby	therefore
therein	theres	thereupon	these	they
they'd	they'll	they're	they've	think
third	this	thorough	thoroughly	those
though	three	through	throughout	thru
thus	to	together	too	took
toward	towards	tried	tries	truly
try	trying	twice	two	un
under	unfortunately	unless	unlikely	until
unto	up	upon	us	use
used	useful	uses	using	usually
value	various	very	via	viz
vs	want	wants	was	wasn't
way	we	we'd	we'll	we're
we've	welcome	well	went	were
weren't	what	what's	whatever	when
whence	whenever	where	where's	whereafter
whereas	whereby	wherein	whereupon	wherever
whether	which	while	whither	who
who's	whoever	whole	whom	whose
why	will	willing	wish	with
within	without	won't	wonder	would
wouldn't	yes	yet	you	you'd
you'll	you're	you've	your	yours
yourself	yourselves	zero";

$list .= "  jwh oso sih ";

$list = normalizationPartOne($list);
$stopWords = explode(" ", $list);
//var_dump($stopWords);
$GLOBALS["stopWords"] = $stopWords;