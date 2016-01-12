<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.8 (Build 35) (http://www.copasi.org) at 2013-04-08 12:42:07 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="1" versionMinor="0" versionDevel="35">
  <ListOfFunctions>
    <Function key="Function_43" name="function_4_Glucose in" type="UserDefined" reversible="unspecified">
      <Expression>
        cytoplasm*(Vm1-Ki1G6P*G6P)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_266" name="G6P" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_258" name="Ki1G6P" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_254" name="Vm1" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_264" name="cytoplasm" order="3" role="volume"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="function_4_Hexokinase" type="UserDefined" reversible="unspecified">
      <Expression>
        Vm2/(1+Km2Glc/Glci+Km2ATP/ATP+Ks2Glc*Km2ATP/(Glci*ATP))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_272" name="ATP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_268" name="Glci" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_270" name="Km2ATP" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_246" name="Km2Glc" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_274" name="Ks2Glc" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_267" name="Vm2" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="function_4_Trehalose and Glycogen formation" type="UserDefined" reversible="unspecified">
      <Expression>
        1.1*Vm3*G6P^n3/(K3Gly^n3+G6P^n3)/(1+Km30/0.7*(1+Km3G6P/G6P))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_271" name="G6P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_276" name="K3Gly" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_278" name="Km30" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_280" name="Km3G6P" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_275" name="Vm3" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_262" name="n3" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="function_4_Phosphofructokinase" type="UserDefined" reversible="unspecified">
      <Expression>
        Vm4*g4R*0.3*G6P/K4F6P*ATP/K4ATP*(1+0.3*G6P/K4F6P+ATP/K4ATP+g4R*0.3*G6P/K4F6P*ATP/K4ATP)/((1+0.3*G6P/K4F6P+ATP/K4ATP+g4R*0.3*G6P/K4F6P*ATP/K4ATP)^2+L40*((1+c4AMP*(3-ATP-0.5*(-ATP+(12*ATP-3*ATP^2)^0.5))/K4AMP)/(1+(3-ATP-0.5*(-ATP+(12*ATP-3*ATP^2)^0.5))/K4AMP))^2*(1+c4F6P*0.3*G6P/K4F6P+c4ATP*ATP/K4ATP+gT*c4F6P*0.3*G6P/K4F6P*c4ATP*ATP/K4ATP)^2)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_284" name="ATP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_269" name="G6P" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_292" name="K4AMP" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_286" name="K4ATP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_282" name="K4F6P" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_288" name="L40" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_281" name="Vm4" order="6" role="constant"/>
        <ParameterDescription key="FunctionParameter_290" name="c4AMP" order="7" role="constant"/>
        <ParameterDescription key="FunctionParameter_296" name="c4ATP" order="8" role="constant"/>
        <ParameterDescription key="FunctionParameter_294" name="c4F6P" order="9" role="constant"/>
        <ParameterDescription key="FunctionParameter_277" name="g4R" order="10" role="constant"/>
        <ParameterDescription key="FunctionParameter_298" name="gT" order="11" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="function_4_GAPD" type="UserDefined" reversible="unspecified">
      <Expression>
        Vm5/(1+K5G3P/(0.01*FDP)+(K5NAD/NAD+K5G3P*K5NAD/(NAD*0.01*FDP)+K5G3P*K5NAD*NADH/(NAD*0.01*FDP*K5NADH))*(1+0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K5ADP+(3-ATP-0.5*(-ATP+(12*ATP-3*ATP^2)^0.5))/K5AMP+ATP/K5ATP))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_302" name="ATP" order="0" role="product"/>
        <ParameterDescription key="FunctionParameter_291" name="FDP" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_304" name="K5ADP" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_306" name="K5AMP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_308" name="K5ATP" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_295" name="K5G3P" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_287" name="K5NAD" order="6" role="constant"/>
        <ParameterDescription key="FunctionParameter_300" name="K5NADH" order="7" role="constant"/>
        <ParameterDescription key="FunctionParameter_283" name="NAD" order="8" role="constant"/>
        <ParameterDescription key="FunctionParameter_265" name="NADH" order="9" role="constant"/>
        <ParameterDescription key="FunctionParameter_299" name="Vm5" order="10" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="function_4_Pyruvate kinase" type="UserDefined" reversible="unspecified">
      <Expression>
        Vm6*(PEP/K6PEP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)*(g6R*(1+PEP/K6PEP+0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6R*PEP/K6PEP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)+q6*L60*((1+c6FDP*FDP/K6FDP)/(1+FDP/K6FDP))^2*g6T*c6PEP*PEP/K6PEP*c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP*(1+c6PEP*PEP/K6PEP+c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6T*c6PEP*PEP/K6PEP*c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP))/((1+9.55*10^-9/h6)*((1+PEP/K6PEP+0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6R*PEP/K6PEP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)^2+L60*((1+c6FDP*FDP/K6FDP)/(1+FDP/K6FDP))^2*(1+c6PEP*PEP/K6PEP+c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6T*c6PEP*PEP/K6PEP*c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)^2))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_273" name="ATP" order="0" role="product"/>
        <ParameterDescription key="FunctionParameter_317" name="FDP" order="1" role="modifier"/>
        <ParameterDescription key="FunctionParameter_289" name="K6ADP" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_319" name="K6FDP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_301" name="K6PEP" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_313" name="L60" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_305" name="PEP" order="6" role="substrate"/>
        <ParameterDescription key="FunctionParameter_309" name="Vm6" order="7" role="constant"/>
        <ParameterDescription key="FunctionParameter_325" name="c6ADP" order="8" role="constant"/>
        <ParameterDescription key="FunctionParameter_315" name="c6FDP" order="9" role="constant"/>
        <ParameterDescription key="FunctionParameter_323" name="c6PEP" order="10" role="constant"/>
        <ParameterDescription key="FunctionParameter_297" name="g6R" order="11" role="constant"/>
        <ParameterDescription key="FunctionParameter_321" name="g6T" order="12" role="constant"/>
        <ParameterDescription key="FunctionParameter_327" name="h6" order="13" role="constant"/>
        <ParameterDescription key="FunctionParameter_311" name="q6" order="14" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="function_4_Glycerol synthesis" type="UserDefined" reversible="unspecified">
      <Expression>
        Vm7*(PEP/K6PEP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)*(g6R*(1+PEP/K6PEP+0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6R*PEP/K6PEP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)+q6*L60*((1+c6FDP*FDP/K6FDP)/(1+FDP/K6FDP))^2*g6T*c6PEP*PEP/K6PEP*c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP*(1+c6PEP*PEP/K6PEP+c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6T*c6PEP*PEP/K6PEP*c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP))/((1+9.55*10^-9/h6)*((1+PEP/K6PEP+0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6R*PEP/K6PEP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)^2+L60*((1+c6FDP*FDP/K6FDP)/(1+FDP/K6FDP))^2*(1+c6PEP*PEP/K6PEP+c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP+g6T*c6PEP*PEP/K6PEP*c6ADP*0.5*(-ATP+(12*ATP-3*ATP^2)^0.5)/K6ADP)^2))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_316" name="ATP" order="0" role="modifier"/>
        <ParameterDescription key="FunctionParameter_332" name="FDP" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_312" name="K6ADP" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_334" name="K6FDP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_320" name="K6PEP" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_307" name="L60" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_324" name="PEP" order="6" role="modifier"/>
        <ParameterDescription key="FunctionParameter_328" name="Vm7" order="7" role="constant"/>
        <ParameterDescription key="FunctionParameter_340" name="c6ADP" order="8" role="constant"/>
        <ParameterDescription key="FunctionParameter_330" name="c6FDP" order="9" role="constant"/>
        <ParameterDescription key="FunctionParameter_338" name="c6PEP" order="10" role="constant"/>
        <ParameterDescription key="FunctionParameter_293" name="g6R" order="11" role="constant"/>
        <ParameterDescription key="FunctionParameter_336" name="g6T" order="12" role="constant"/>
        <ParameterDescription key="FunctionParameter_342" name="h6" order="13" role="constant"/>
        <ParameterDescription key="FunctionParameter_279" name="q6" order="14" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_50" name="function_4_ATPase" type="UserDefined" reversible="true">
      <Expression>
        Vm8*ATP
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_339" name="ATP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_343" name="Vm8" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_1" name="Galazzo1990_FermentationPathwayKinetics" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="mmol" type="deterministic" avogadroConstant="6.02214179e+023">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <rdf:Description rdf:about="#Model_1">
    <dcterms:bibliographicCitation>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <CopasiMT:isDescribedBy rdf:resource="urn:miriam:doi:10.1016%2F0141-0229%2890%2990033-M"/>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:bibliographicCitation>
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2006-08-13T19:32:16Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
    <dcterms:creator>
      <rdf:Bag>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>jls@sun.ac.za</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Snoep</vCard:Family>
                <vCard:Given>Jacky L</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>Stellenbosh University</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>hdharuri@cds.caltech.edu</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Dharuri</vCard:Family>
                <vCard:Given>Harish</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>California Institute of Technology</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
        <rdf:li>
          <rdf:Description>
            <vCard:EMAIL>lukas@ebi.ac.uk</vCard:EMAIL>
            <vCard:N>
              <rdf:Description>
                <vCard:Family>Endler</vCard:Family>
                <vCard:Given>Lukas</vCard:Given>
              </rdf:Description>
            </vCard:N>
            <vCard:ORG>
              <rdf:Description>
                <vCard:Orgname>EMBL-EBI</vCard:Orgname>
              </rdf:Description>
            </vCard:ORG>
          </rdf:Description>
        </rdf:li>
      </rdf:Bag>
    </dcterms:creator>
    <dcterms:modified>
      <rdf:Description>
        <dcterms:W3CDTF>2011-07-26T23:53:21Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:modified>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:biomodels.db:BIOMD0000000063"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:biomodels.db:MODEL6624154196"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.pathway:sce00010"/>
        <rdf:li rdf:resource="urn:miriam:taxonomy:4932"/>
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:reactome:REACT_723"/>
      </rdf:Bag>
    </CopasiMT:isHomologTo>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006113"/>
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <body xmlns="http://www.w3.org/1999/xhtml">
    <p>
      This a model from the article:
      <br />
    <strong> 
Fermentation pathway kinetics and metabolic flux control in suspended and immobilized Saccharomyces cerevisiae 
</strong>
    <br />
Jorge L. Galazzo and James E. Bailey
      <em>Enzyme and Microbial Technology</em>Volume 12, Issue 3, 1990, Pages 162-172. 
      <br />
      DOI:<a href="dx.doi.org/10.1016/0141-0229(90)90033-M">10.1016/0141-0229(90)90033-M</a>
    <br />
    <strong>Abstract:</strong>
    <br />
Measurements of rates of glucose uptake and of glycerol and ethanol formation combined with knowledge of the metabolic pathways involved in S. cerevisiae were employed to obtain in vivo rates of reaction catalysed by pathway enzymes for suspended and alginate-entrapped cells at pH 4.5 and 5.5. Intracellular concentrations of substrates and effectors for most key pathway enzymes were estimated from in vivo phosphorus-31 nuclear magnetic resonance measurements. These data show the validity in vivo of kinetic models previously proposed for phosphofructokinase and pyruvate kinase based on in vitro studies. Kinetic representations of hexokinase, glycogen synthetase, and glyceraldehyde 3-phosphate dehydrogenase, which incorporate major regulatory properties of these enzymes, are all consistent with the in vivo data. This detailed model of pathway kinetics and these data on intracellular metabolite concentrations allow evaluation of flux-control coefficients for all key enzymes involved in glucose catabolism under the four different cell environments examined. This analysis indicates that alginate entrapment increases the glucose uptake rate and shifts the step most influencing ethanol production from glucose uptake to phosphofructokinase. The rate of ATP utilization in these nongrowing cells strongly limits ethanol production at pH 5.5 but is relatively insignificant at pH 4.5.
   </p>
    <p align="left">
      <font face="Arial, Helvetica, sans-serif">
        <b>
          <a href="http://www.sbml.org/">SBML</a> level 2 code generated for the JWS Online project by Jacky Snoep using 
              
              <a href="http://pysces.sourceforge.net/">PySCeS</a>
          <br />
Run this model online at 
              <a href="http://jjj.biochem.sun.ac.za/">http://jjj.biochem.sun.ac.za</a>
          <br />
To cite JWS Online please refer to: Olivier, B.G. and Snoep, J.L. (2004) 
              <a href="http://bioinformatics.oupjournals.org/cgi/content/abstract/20/13/2143">Web-based 
modelling using JWS Online</a>, Bioinformatics, 20:2143-2144
 </b>
        </font>
      </p>
      <p align="right">
        <font color="#FFFFFF">.</font>
      </p>
      <p align="right">
        <font color="#FFFFFF">.</font>
      </p>
      <p align="right">
        <font color="#FFFFFF">.</font>
      </p>
      <p align="right">
        <font color="#FFFFFF">.</font>
      </p>
      <p align="right">
        <font color="#FFFFFF">.</font>
      </p>
      <p align="right">
        <font color="#FFFFFF">.</font>
      </p>
      <p>
        <u> Biomodels Curation:</u> The model reproduces Fig 2 of the paper. However, it appears that the figures are swapped, hence the plot for V/Vmax vs Glucose actually represnts V/Vmax vs ATP and the vice versa is true for the other figure. The rate of hexokinase reaction that is obtained upon simulation of the model is 17.24 mM/min, therefore V/Vmax has a value of 17.24/68.5=0.25. For steady state values of Glucose and ATP (0.038 and 1.213 mM respectively), the V/Vmax values correctly correspond to 0.25, if we were to assume that the figures are swapped. </p>
        <p>
          <u> BioModels Curation updated on 25<sup>th</sup> November 2010: </u>  Figure 3 of the reference publication has been reproduced and added as a curation figure for the model.</p>
          <p>This model originates from BioModels Database: A Database of Annotated Published Models (http://www.ebi.ac.uk/biomodels/). It is copyright (c) 2005-2011 The BioModels.net Team.<br />
For more information see the <a href="http://www.ebi.ac.uk/biomodels/legal.html" target="_blank">terms of use</a>.<br />
To cite BioModels Database, please use: <a href="http://www.ncbi.nlm.nih.gov/pubmed/20587024" target="_blank">Li C, Donizelli M, Rodriguez N, Dharuri H, Endler L, Chelliah V, Li L, He E, Henry A, Stefan MI, Snoep JL, Hucka M, Le Novère N, Laibe C (2010) BioModels Database: An enhanced, curated and annotated resource for published quantitative kinetic models. BMC Syst Biol., 4:92.</a>
        </p>
      </body>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_0" name="Extracellular" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_0">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005576" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
      <Compartment key="Compartment_1" name="Cytoplasm" simulationType="fixed" dimensionality="3">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Compartment_1">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005737" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_0" name="Glucose outside the cell" simulationType="fixed" compartment="Compartment_0">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_0">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00293" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A17234" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_1" name="Glucose inside the cell" simulationType="reactions" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_1">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00293" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A17234" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_2" name="ATP" simulationType="reactions" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_2">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00002" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A15422" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_3" name="Glucose 6-phosphate" simulationType="reactions" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_3">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00668" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A17665" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_4" name="Fructose 1,6-phosphate" simulationType="reactions" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_4">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00354" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A16905" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_5" name="Phosphoenol pyruvate" simulationType="reactions" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_5">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00074" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A18021" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_6" name="Glycerol" simulationType="fixed" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_6">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00116" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A17754" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_7" name="Ethanol" simulationType="fixed" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_7">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00469" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A16236" />
      </rdf:Bag>
    </CopasiMT:is>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
      <Metabolite key="Metabolite_8" name="Glycogen and Trehalose" simulationType="fixed" compartment="Compartment_1">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Metabolite_8">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A27082" />
        <rdf:li rdf:resource="urn:miriam:obo.chebi:CHEBI%3A28087" />
      </rdf:Bag>
    </CopasiMT:hasPart>
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C00182" />
        <rdf:li rdf:resource="urn:miriam:kegg.compound:C01083" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_0" name="VappGly" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[Trehalose and Glycogen formation_Vm3],Reference=Value&gt;*&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Vector=Metabolites[Glucose 6-phosphate],Reference=Concentration&gt;^&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[Trehalose and Glycogen formation_n3],Reference=Value&gt;/(&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[Trehalose and Glycogen formation_K3Gly],Reference=Value&gt;^&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[Trehalose and Glycogen formation_n3],Reference=Value&gt;+&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Vector=Metabolites[Glucose 6-phosphate],Reference=Concentration&gt;^&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[Trehalose and Glycogen formation_n3],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_1" name="VratioVmax_ATP" simulationType="assignment">
        <Expression>
          &lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Hexokinase],Reference=Flux&gt;/(&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Reference=Volume&gt;*&lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[Hexokinase_Vm2],Reference=Value&gt;)
        </Expression>
      </ModelValue>
      <ModelValue key="ModelValue_2" name="Trehalose and Glycogen formation_Vm3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_3" name="Trehalose and Glycogen formation_n3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_4" name="Trehalose and Glycogen formation_K3Gly" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_5" name="Hexokinase_Vm2" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_0" name="Glucose in" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_0">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0046323" />
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:reactome:REACT_2092" />
      </rdf:Bag>
    </CopasiMT:isHomologTo>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_0" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_1621" name="Vm1" value="19.7"/>
          <Constant key="Parameter_1620" name="Ki1G6P" value="3.7"/>
        </ListOfConstants>
        <KineticLaw function="Function_43">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Parameter_1620"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="Parameter_1621"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="Hexokinase" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_1">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.1.2" />
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R00299" />
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:reactome:REACT_1318" />
      </rdf:Bag>
    </CopasiMT:isHomologTo>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_2" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1619" name="Vm2" value="68.5"/>
          <Constant key="Parameter_1618" name="Km2Glc" value="0.11"/>
          <Constant key="Parameter_1617" name="Km2ATP" value="0.1"/>
          <Constant key="Parameter_1616" name="Ks2Glc" value="0.0062"/>
        </ListOfConstants>
        <KineticLaw function="Function_44">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Parameter_1617"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="Parameter_1618"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Parameter_1616"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Parameter_1619"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="Trehalose and Glycogen formation" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_2">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005978" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0005992" />
      </rdf:Bag>
    </CopasiMT:hasPart>
    <CopasiMT:isHomologTo>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:reactome:REACT_1736" />
      </rdf:Bag>
    </CopasiMT:isHomologTo>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_2" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_8" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1615" name="Vm3" value="14.31"/>
          <Constant key="Parameter_1614" name="n3" value="8.25"/>
          <Constant key="Parameter_1613" name="K3Gly" value="2"/>
          <Constant key="Parameter_1612" name="Km30" value="1"/>
          <Constant key="Parameter_1611" name="Km3G6P" value="1.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_45">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Parameter_1613"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Parameter_1612"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="Parameter_1611"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Parameter_1615"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="Parameter_1614"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="Phosphofructokinase" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_3">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:reactome:REACT_1164" />
        <rdf:li rdf:resource="urn:miriam:reactome:REACT_736" />
      </rdf:Bag>
    </CopasiMT:hasPart>
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R00756" />
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R00771" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_2" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1610" name="Vm4" value="31.7"/>
          <Constant key="Parameter_1609" name="g4R" value="10"/>
          <Constant key="Parameter_1608" name="K4F6P" value="1"/>
          <Constant key="Parameter_1607" name="K4ATP" value="0.06"/>
          <Constant key="Parameter_1606" name="L40" value="3342"/>
          <Constant key="Parameter_1605" name="c4AMP" value="0.019"/>
          <Constant key="Parameter_1604" name="K4AMP" value="0.025"/>
          <Constant key="Parameter_1603" name="c4F6P" value="0.0005"/>
          <Constant key="Parameter_1602" name="c4ATP" value="1"/>
          <Constant key="Parameter_1601" name="gT" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_46">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Parameter_1604"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_286">
              <SourceParameter reference="Parameter_1607"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="Parameter_1608"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="Parameter_1606"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Parameter_1610"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Parameter_1605"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_296">
              <SourceParameter reference="Parameter_1602"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Parameter_1603"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Parameter_1609"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_298">
              <SourceParameter reference="Parameter_1601"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="GAPD" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_4">
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R00658" />
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R01015" />
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R01061" />
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R01070" />
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R01512" />
        <rdf:li rdf:resource="urn:miriam:kegg.reaction:R01518" />
      </rdf:Bag>
    </CopasiMT:hasPart>
    <CopasiMT:hasPart>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:1.2.1.12" />
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.2.3" />
        <rdf:li rdf:resource="urn:miriam:ec-code:4.1.2.13" />
        <rdf:li rdf:resource="urn:miriam:ec-code:4.2.1.11" />
        <rdf:li rdf:resource="urn:miriam:ec-code:5.3.1.1" />
        <rdf:li rdf:resource="urn:miriam:ec-code:5.4.2.1" />
      </rdf:Bag>
    </CopasiMT:hasPart>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_2" stoichiometry="2"/>
          <Product metabolite="Metabolite_5" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1600" name="Vm5" value="49.9"/>
          <Constant key="Parameter_1599" name="K5G3P" value="0.0025"/>
          <Constant key="Parameter_1598" name="K5NAD" value="0.18"/>
          <Constant key="Parameter_1597" name="NAD" value="1.91939"/>
          <Constant key="Parameter_1596" name="NADH" value="0.0806142"/>
          <Constant key="Parameter_1595" name="K5NADH" value="0.0003"/>
          <Constant key="Parameter_1594" name="K5ADP" value="1.5"/>
          <Constant key="Parameter_1593" name="K5AMP" value="1.1"/>
          <Constant key="Parameter_1592" name="K5ATP" value="2.5"/>
        </ListOfConstants>
        <KineticLaw function="Function_47">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_302">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_291">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_304">
              <SourceParameter reference="Parameter_1594"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_306">
              <SourceParameter reference="Parameter_1593"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_308">
              <SourceParameter reference="Parameter_1592"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_295">
              <SourceParameter reference="Parameter_1599"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Parameter_1598"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_300">
              <SourceParameter reference="Parameter_1595"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Parameter_1597"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Parameter_1596"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_299">
              <SourceParameter reference="Parameter_1600"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="Pyruvate kinase" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_5">
    <CopasiMT:is>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:2.7.1.40" />
      </rdf:Bag>
    </CopasiMT:is>
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0043458" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_2" stoichiometry="1"/>
          <Product metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_1591" name="Vm6" value="3440"/>
          <Constant key="Parameter_1590" name="K6PEP" value="0.00793966"/>
          <Constant key="Parameter_1589" name="K6ADP" value="5"/>
          <Constant key="Parameter_1588" name="g6R" value="0.1"/>
          <Constant key="Parameter_1587" name="q6" value="1"/>
          <Constant key="Parameter_1586" name="L60" value="164.084"/>
          <Constant key="Parameter_1585" name="c6FDP" value="0.01"/>
          <Constant key="Parameter_1584" name="K6FDP" value="0.2"/>
          <Constant key="Parameter_1583" name="g6T" value="1"/>
          <Constant key="Parameter_1582" name="c6PEP" value="0.000158793"/>
          <Constant key="Parameter_1581" name="c6ADP" value="1"/>
          <Constant key="Parameter_1580" name="h6" value="1.14815e-007"/>
        </ListOfConstants>
        <KineticLaw function="Function_48">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_317">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="Parameter_1589"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_319">
              <SourceParameter reference="Parameter_1584"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_301">
              <SourceParameter reference="Parameter_1590"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_313">
              <SourceParameter reference="Parameter_1586"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_305">
              <SourceParameter reference="Metabolite_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_309">
              <SourceParameter reference="Parameter_1591"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_325">
              <SourceParameter reference="Parameter_1581"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_315">
              <SourceParameter reference="Parameter_1585"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_323">
              <SourceParameter reference="Parameter_1582"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_297">
              <SourceParameter reference="Parameter_1588"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_321">
              <SourceParameter reference="Parameter_1583"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_327">
              <SourceParameter reference="Parameter_1580"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_311">
              <SourceParameter reference="Parameter_1587"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_6" name="Glycerol synthesis" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_6">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0006114" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_4" stoichiometry="0.5"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_6" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_5" stoichiometry="1"/>
          <Modifier metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_1579" name="Vm7" value="203"/>
          <Constant key="Parameter_1578" name="K6PEP" value="0.00793966"/>
          <Constant key="Parameter_1577" name="K6ADP" value="5"/>
          <Constant key="Parameter_1576" name="g6R" value="0.1"/>
          <Constant key="Parameter_1575" name="q6" value="1"/>
          <Constant key="Parameter_1574" name="L60" value="164.084"/>
          <Constant key="Parameter_1573" name="c6FDP" value="0.01"/>
          <Constant key="Parameter_1572" name="K6FDP" value="0.2"/>
          <Constant key="Parameter_1571" name="g6T" value="1"/>
          <Constant key="Parameter_1570" name="c6PEP" value="0.000158793"/>
          <Constant key="Parameter_1569" name="c6ADP" value="1"/>
          <Constant key="Parameter_1568" name="h6" value="1.14815e-007"/>
        </ListOfConstants>
        <KineticLaw function="Function_49">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_316">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_332">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_312">
              <SourceParameter reference="Parameter_1577"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_334">
              <SourceParameter reference="Parameter_1572"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_320">
              <SourceParameter reference="Parameter_1578"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_307">
              <SourceParameter reference="Parameter_1574"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_324">
              <SourceParameter reference="Metabolite_5"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_328">
              <SourceParameter reference="Parameter_1579"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_340">
              <SourceParameter reference="Parameter_1569"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_330">
              <SourceParameter reference="Parameter_1573"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_338">
              <SourceParameter reference="Parameter_1570"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Parameter_1576"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_336">
              <SourceParameter reference="Parameter_1571"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_342">
              <SourceParameter reference="Parameter_1568"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Parameter_1575"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_7" name="ATPase" reversible="true">
        <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Reaction_7">
    <CopasiMT:isVersionOf>
      <rdf:Bag>
        <rdf:li rdf:resource="urn:miriam:ec-code:3.6.1.3" />
        <rdf:li rdf:resource="urn:miriam:obo.go:GO%3A0016887" />
      </rdf:Bag>
    </CopasiMT:isVersionOf>
  </rdf:Description>
</rdf:RDF>
        </MiriamAnnotation>
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfConstants>
          <Constant key="Parameter_1567" name="Vm8" value="25.1"/>
        </ListOfConstants>
        <KineticLaw function="Function_50">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_339">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_343">
              <SourceParameter reference="Parameter_1567"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_1"/>
      <StateTemplateVariable objectReference="Metabolite_2"/>
      <StateTemplateVariable objectReference="Metabolite_5"/>
      <StateTemplateVariable objectReference="Metabolite_3"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Metabolite_4"/>
      <StateTemplateVariable objectReference="ModelValue_0"/>
      <StateTemplateVariable objectReference="ModelValue_1"/>
      <StateTemplateVariable objectReference="Metabolite_0"/>
      <StateTemplateVariable objectReference="Metabolite_6"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Metabolite_8"/>
      <StateTemplateVariable objectReference="ModelValue_2"/>
      <StateTemplateVariable objectReference="ModelValue_3"/>
      <StateTemplateVariable objectReference="ModelValue_4"/>
      <StateTemplateVariable objectReference="ModelValue_5"/>
      <StateTemplateVariable objectReference="Compartment_0"/>
      <StateTemplateVariable objectReference="Compartment_1"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 7.1663487301e+020 5.721034700500001e+018 6.088385349689999e+020 2.077638917550001e+019 5.506646452776001e+021 0.05126024903774349 NaN 6.022141790000001e+020 0 0 0 14.31 8.25 2 68.5 1 1 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_16" name="Optimization" type="optimization" scheduled="true" updateModel="true">
      <Report reference="Report_10" target="./report.log" append="1"/>
      <Problem>
        <Parameter name="Subtask" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <ParameterText name="ObjectiveExpression" type="expression">
          &lt;CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Pyruvate kinase],Reference=Flux&gt;
        </ParameterText>
        <Parameter name="Maximize" type="bool" value="1"/>
        <Parameter name="Randomize Start Values" type="bool" value="1"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">

          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.251"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[ATPase],ParameterGroup=Parameters,Parameter=Vm8,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="25.1"/>
            <Parameter name="UpperBound" type="cn" value="251"/>
          </ParameterGroup>

          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.499"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[GAPD],ParameterGroup=Parameters,Parameter=Vm5,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="49.9"/>
            <Parameter name="UpperBound" type="cn" value="499"/>
          </ParameterGroup>

          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.197"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Glucose in],ParameterGroup=Parameters,Parameter=Vm1,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="19.7"/>
            <Parameter name="UpperBound" type="cn" value="197"/>
          </ParameterGroup>

          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.685"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Hexokinase],ParameterGroup=Parameters,Parameter=Vm2,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="68.5"/>
            <Parameter name="UpperBound" type="cn" value="685"/>
          </ParameterGroup>

          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.317"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Phosphofructokinase],ParameterGroup=Parameters,Parameter=Vm4,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="31.7"/>
            <Parameter name="UpperBound" type="cn" value="317"/>
          </ParameterGroup>

          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="34.4"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Pyruvate kinase],ParameterGroup=Parameters,Parameter=Vm6,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="3440"/>
            <Parameter name="UpperBound" type="cn" value="34400"/>
          </ParameterGroup>

        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
      </Problem>
      <Method name="Particle Swarm" type="ParticleSwarm">
        <Parameter name="Iteration Limit" type="unsignedInteger" value="2000"/>
        <Parameter name="Swarm Size" type="unsignedInteger" value="50"/>
        <Parameter name="Std. Deviation" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
      <Method name="test method" type="TestMethod">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_8" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_9" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_10" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=CPU time"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=maximum real part"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Timer=CPU Time"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Steady-State],Eigen Values=Eigenvalues of reduced system Jacobian,Reference=Maximum real part"/>
      </Body>
    </Report>
    <Report key="Report_11" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_12" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_13" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_14" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_15" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
  </ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[&quot;Glucose inside the cell&quot;]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Vector=Metabolites[Glucose inside the cell],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[ATP]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Vector=Metabolites[ATP],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[&quot;Glucose 6-phosphate&quot;]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Vector=Metabolites[Glucose 6-phosphate],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[&quot;Fructose 1,6-phosphate&quot;]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Vector=Metabolites[Fructose 1\,6-phosphate],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[&quot;Phosphoenol pyruvate&quot;]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Compartments[Cytoplasm],Vector=Metabolites[Phosphoenol pyruvate],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[VappGly]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[VappGly],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Values[VratioVmax_ATP]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Values[VratioVmax_ATP],Reference=Value"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="BIOMD0000000063.xml">
    <SBMLMap SBMLid="ATP" COPASIkey="Metabolite_2"/>
    <SBMLMap SBMLid="Carbo" COPASIkey="Metabolite_8"/>
    <SBMLMap SBMLid="EtOH" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="FDP" COPASIkey="Metabolite_4"/>
    <SBMLMap SBMLid="G6P" COPASIkey="Metabolite_3"/>
    <SBMLMap SBMLid="Glci" COPASIkey="Metabolite_1"/>
    <SBMLMap SBMLid="Glco" COPASIkey="Metabolite_0"/>
    <SBMLMap SBMLid="Gly" COPASIkey="Metabolite_6"/>
    <SBMLMap SBMLid="PEP" COPASIkey="Metabolite_5"/>
    <SBMLMap SBMLid="VappGly" COPASIkey="ModelValue_0"/>
    <SBMLMap SBMLid="Vatpase" COPASIkey="Reaction_7"/>
    <SBMLMap SBMLid="Vgapd" COPASIkey="Reaction_4"/>
    <SBMLMap SBMLid="Vgol" COPASIkey="Reaction_6"/>
    <SBMLMap SBMLid="Vhk" COPASIkey="Reaction_1"/>
    <SBMLMap SBMLid="Vin" COPASIkey="Reaction_0"/>
    <SBMLMap SBMLid="Vpfk" COPASIkey="Reaction_3"/>
    <SBMLMap SBMLid="Vpk" COPASIkey="Reaction_5"/>
    <SBMLMap SBMLid="Vpol" COPASIkey="Reaction_2"/>
    <SBMLMap SBMLid="VratioVmax" COPASIkey="ModelValue_1"/>
    <SBMLMap SBMLid="cytoplasm" COPASIkey="Compartment_1"/>
    <SBMLMap SBMLid="extracellular" COPASIkey="Compartment_0"/>
    <SBMLMap SBMLid="parameter_4" COPASIkey="ModelValue_2"/>
    <SBMLMap SBMLid="parameter_5" COPASIkey="ModelValue_3"/>
    <SBMLMap SBMLid="parameter_6" COPASIkey="ModelValue_4"/>
    <SBMLMap SBMLid="parameter_7" COPASIkey="ModelValue_5"/>
  </SBMLReference>
</COPASI>
