<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.8 (Build 35) (http://www.copasi.org) at 2013-04-08 12:56:18 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="1" versionMinor="0" versionDevel="35">
  <ListOfFunctions>
    <Function key="Function_43" name="function_4_Glucose Mixed flow to extracellular medium" type="UserDefined" reversible="true">
      <Expression>
        k0*(GlcX0-GlcX)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_258" name="GlcX" order="0" role="product"/>
        <ParameterDescription key="FunctionParameter_254" name="GlcX0" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_264" name="k0" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_44" name="function_4_Ethanol out" type="UserDefined" reversible="true">
      <Expression>
        k13/Yvol*(cytosol*EtOH-extracellular*EtOHX)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_269" name="EtOH" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_273" name="EtOHX" order="1" role="product"/>
        <ParameterDescription key="FunctionParameter_262" name="Yvol" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_267" name="cytosol" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_271" name="extracellular" order="4" role="volume"/>
        <ParameterDescription key="FunctionParameter_265" name="k13" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_45" name="function_4_Ethanol flow" type="UserDefined" reversible="true">
      <Expression>
        k0*EtOHX
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_270" name="EtOHX" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_274" name="k0" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_46" name="function_4_Glycerol out" type="UserDefined" reversible="true">
      <Expression>
        k16/Yvol*(cytosol*Glyc-extracellular*GlycX)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_277" name="Glyc" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_281" name="GlycX" order="1" role="product"/>
        <ParameterDescription key="FunctionParameter_266" name="Yvol" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_275" name="cytosol" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_279" name="extracellular" order="4" role="volume"/>
        <ParameterDescription key="FunctionParameter_268" name="k16" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_47" name="function_4_Glycerol flow" type="UserDefined" reversible="true">
      <Expression>
        k0*GlycX
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_278" name="GlycX" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_282" name="k0" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_48" name="function_4_Acetaldehyde out" type="UserDefined" reversible="true">
      <Expression>
        k18/Yvol*(cytosol*ACA-extracellular*ACAX)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_285" name="ACA" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_289" name="ACAX" order="1" role="product"/>
        <ParameterDescription key="FunctionParameter_246" name="Yvol" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_283" name="cytosol" order="3" role="volume"/>
        <ParameterDescription key="FunctionParameter_287" name="extracellular" order="4" role="volume"/>
        <ParameterDescription key="FunctionParameter_276" name="k18" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_49" name="function_4_Acetaldehyde flow" type="UserDefined" reversible="true">
      <Expression>
        k0*ACAX
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_286" name="ACAX" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_290" name="k0" order="1" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_50" name="function_4_Cyanide-Acetaldehyde flow" type="UserDefined" reversible="true">
      <Expression>
        k20*ACAX*CNX
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_272" name="ACAX" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_291" name="CNX" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_284" name="k20" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_51" name="function_4_Cyanide flow" type="UserDefined" reversible="true">
      <Expression>
        k0*(CNX0-CNX)
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_294" name="CNX" order="0" role="product"/>
        <ParameterDescription key="FunctionParameter_288" name="CNX0" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_292" name="k0" order="2" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_52" name="Mass action variable concentr (rev)" type="UserDefined" reversible="true">
      <Expression>
        Kc * ( kf * S1 * S2 - kr * P1 * P2 )
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_295" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_280" name="kf" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_297" name="S1" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_299" name="S2" order="3" role="substrate"/>
        <ParameterDescription key="FunctionParameter_301" name="kr" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_303" name="P1" order="5" role="product"/>
        <ParameterDescription key="FunctionParameter_305" name="P2" order="6" role="product"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_53" name="IM_Phosphoglucoisomerase_reversible" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Kf*G6P/(K4G6P+G6P+K4G6P/K4F6P*F6P)-Kr*(F6P/K4eq)/(K4G6P+G6P+K4G6P/K4F6P*F6P))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_306" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_302" name="Kf" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_298" name="G6P" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_293" name="K4G6P" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_308" name="K4F6P" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_310" name="F6P" order="5" role="product"/>
        <ParameterDescription key="FunctionParameter_312" name="Kr" order="6" role="constant"/>
        <ParameterDescription key="FunctionParameter_314" name="K4eq" order="7" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_54" name="IM_Triosephosphate" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Kf*DHAP/(K7DHAP+DHAP+K7DHAP/K7GAP*GAP)-Kr*(GAP/K7eq)/(K7DHAP+DHAP+K7DHAP/K7GAP*GAP))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_315" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_311" name="Kf" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_307" name="DHAP" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_300" name="K7DHAP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_316" name="K7GAP" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_318" name="GAP" order="5" role="product"/>
        <ParameterDescription key="FunctionParameter_320" name="Kr" order="6" role="constant"/>
        <ParameterDescription key="FunctionParameter_322" name="K7eq" order="7" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_55" name="IM_Glyceraldehyde3ph" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Kf*GAP*NAD/K8GAP/K8NAD/((1+GAP/K8GAP+BPG/K8BPG)*(1+NAD/K8NAD+NADH/K8NADH))-Kr*BPG*NADH/K8eq/K8GAP/K8NAD/((1+GAP/K8GAP+BPG/K8BPG)*(1+NAD/K8NAD+NADH/K8NADH)))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_323" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_304" name="GAP" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_309" name="NAD" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_324" name="K8GAP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_326" name="K8NAD" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_328" name="BPG" order="5" role="product"/>
        <ParameterDescription key="FunctionParameter_330" name="K8BPG" order="6" role="constant"/>
        <ParameterDescription key="FunctionParameter_332" name="NADH" order="7" role="product"/>
        <ParameterDescription key="FunctionParameter_334" name="K8NADH" order="8" role="constant"/>
        <ParameterDescription key="FunctionParameter_338" name="K8eq" order="9" role="constant"/>
        <ParameterDescription key="FunctionParameter_319" name="Kf" order="10" role="constant"/>
        <ParameterDescription key="FunctionParameter_336" name="Kr" order="11" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_56" name="IM_GlucUpt" type="UserDefined" reversible="true">
      <Expression>
        Kc*(extracellular*Kf/Yvol*(GlcX/K2Glc/(1+GlcX/K2Glc+(P2*(GlcX/K2Glc)+1)/(P2*(Glc/K2Glc)+1)*(1+Glc/K2Glc+G6P/K2IG6P+Glc*G6P/(K2Glc*K2IIG6P))))-cytosol*Kr/Yvol*(Glc/K2Glc/(1+Glc/K2Glc+(P2*(Glc/K2Glc)+1)/(P2*(GlcX/K2Glc)+1)*(1+GlcX/K2Glc)+G6P/K2IG6P+Glc*G6P/(K2Glc*K2IIG6P))))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_335" name="extracellular" order="0" role="volume"/>
        <ParameterDescription key="FunctionParameter_331" name="Kf" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_327" name="Yvol" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_313" name="GlcX" order="3" role="substrate"/>
        <ParameterDescription key="FunctionParameter_317" name="K2Glc" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_340" name="P2" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_342" name="Glc" order="6" role="product"/>
        <ParameterDescription key="FunctionParameter_344" name="G6P" order="7" role="modifier"/>
        <ParameterDescription key="FunctionParameter_346" name="K2IG6P" order="8" role="constant"/>
        <ParameterDescription key="FunctionParameter_348" name="K2IIG6P" order="9" role="constant"/>
        <ParameterDescription key="FunctionParameter_350" name="cytosol" order="10" role="volume"/>
        <ParameterDescription key="FunctionParameter_352" name="Kr" order="11" role="constant"/>
        <ParameterDescription key="FunctionParameter_339" name="Kc" order="12" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_57" name="IM_Hexokinase" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Km*ATP*Glc/(K3DGlc*K3ATP+K3Glc*ATP+K3ATP*Glc+Glc*ATP))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_353" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_349" name="Km" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_345" name="ATP" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_341" name="Glc" order="3" role="substrate"/>
        <ParameterDescription key="FunctionParameter_296" name="K3DGlc" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_329" name="K3ATP" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_337" name="K3Glc" order="6" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_58" name="IM_Phosphofructokinase" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Km*F6P^2/(K5*(1+kappa5*(ATP/AMP)*(ATP/AMP))+F6P^2))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_343" name="F6P" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_351" name="K5" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_356" name="kappa5" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_358" name="ATP" order="3" role="substrate"/>
        <ParameterDescription key="FunctionParameter_360" name="AMP" order="4" role="modifier"/>
        <ParameterDescription key="FunctionParameter_354" name="Kc" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_325" name="Km" order="6" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_59" name="IM_Aldolase" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Kf*FBP/(K6FBP+FBP+GAP*K6DHAP*Kf/(K6eq*Kf*ratio6)+DHAP*K6GAP*Kf/(K6eq*Kf*ratio6)+FBP*GAP/K6IGAP+GAP*DHAP*Kf/(K6eq*Kf*ratio6))-Kf*GAP*DHAP/K6eq/(K6FBP+FBP+GAP*K6DHAP*Kf/(K6eq*Kf*ratio6)+DHAP*K6GAP*Kf/(K6eq*Kf*ratio6)+FBP*GAP/K6IGAP+GAP*DHAP*Kf/(K6eq*Kf*ratio6)))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_347" name="FBP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_333" name="K6FBP" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_363" name="GAP" order="2" role="product"/>
        <ParameterDescription key="FunctionParameter_365" name="K6DHAP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_367" name="K6eq" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_369" name="ratio6" order="5" role="constant"/>
        <ParameterDescription key="FunctionParameter_371" name="DHAP" order="6" role="product"/>
        <ParameterDescription key="FunctionParameter_373" name="K6GAP" order="7" role="constant"/>
        <ParameterDescription key="FunctionParameter_375" name="K6IGAP" order="8" role="constant"/>
        <ParameterDescription key="FunctionParameter_361" name="Kc" order="9" role="constant"/>
        <ParameterDescription key="FunctionParameter_357" name="Kf" order="10" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_60" name="IM_Pyruvate kinase" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Km*ADP*PEP/((K10PEP+PEP)*(K10ADP+ADP)))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_368" name="ADP" order="0" role="substrate"/>
        <ParameterDescription key="FunctionParameter_364" name="PEP" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_321" name="K10PEP" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_359" name="K10ADP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_376" name="Kc" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_372" name="Km" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_61" name="IM_Pyruvate decarboxylase" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Km*Pyr/(K11+Pyr))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_377" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_362" name="Km" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_370" name="Pyr" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_378" name="K11" order="3" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_62" name="IM_Alcohol dehydrogenase" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Km*ACA*NADH/((K12NADH+NADH)*(K12ACA+ACA)))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_379" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_380" name="ACA" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_382" name="NADH" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_384" name="K12NADH" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_386" name="K12ACA" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_366" name="Km" order="5" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_63" name="IM_Glycerol synthesis" type="UserDefined" reversible="true">
      <Expression>
        Kc*(Km*DHAP/(K15DHAP*(1+K15INADH/NADH*(1+NAD/K15INAD))+DHAP*(1+K15NADH/NADH*(1+NAD/K15INAD))))
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_387" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_383" name="Km" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_355" name="DHAP" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_388" name="K15DHAP" order="3" role="constant"/>
        <ParameterDescription key="FunctionParameter_390" name="K15INADH" order="4" role="constant"/>
        <ParameterDescription key="FunctionParameter_392" name="NADH" order="5" role="substrate"/>
        <ParameterDescription key="FunctionParameter_394" name="NAD" order="6" role="product"/>
        <ParameterDescription key="FunctionParameter_396" name="K15INAD" order="7" role="constant"/>
        <ParameterDescription key="FunctionParameter_398" name="K15NADH" order="8" role="constant"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_64" name="IM_Storage" type="UserDefined" reversible="true">
      <Expression>
        Kc*k22*ATP*G6P
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_399" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_395" name="k22" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_391" name="ATP" order="2" role="substrate"/>
        <ParameterDescription key="FunctionParameter_374" name="G6P" order="3" role="substrate"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_65" name="IM_ATP consumption" type="UserDefined" reversible="true">
      <Expression>
        Kc*k23*ATP
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_381" name="Kc" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_393" name="k23" order="1" role="constant"/>
        <ParameterDescription key="FunctionParameter_385" name="ATP" order="2" role="substrate"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_1" name="Hynne2001 Glycolysis" simulationType="time" timeUnit="min" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="mmol" type="deterministic" avogadroConstant="6.0221415e+023">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Model_1">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2013-04-08T15:37:44Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <Comment>
      <html xmlns="http://www.w3.org/1999/xhtml"><head><meta name="qrichtext" content="1" /></head><body style="font-size:8pt;font-family:MS Shell Dlg">
<p align="right">The model reproduces Fig 6 of the paper. The stoichiometry and rate of reactions involving uptake of metabolites from extracellular medium have been changed corresponding to Yvol (ratio of extracellular volume to cytosolic volume) mentioned in the publication. The extracellular and cytosolic compartments have been set to 1. Concentration of extracellular glucose, GlcX, is set to 6.7 according to the equation for cellular glucose uptake rate in Table 7 of the paper. The model was successfully tested on MathSBML and Jarnac</p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p><a href="http://www.sbml.org/"><span style="font-family:Arial;font-weight:600">SBML</span></a><span style="font-family:Arial;font-weight:600"> level 2 code generated for the JWS Online project by Jacky Snoep using </span><a href="http://pysces.sourceforge.net/"><span style="font-family:Arial;font-weight:600">PySCeS</span></a><span style="font-family:Arial;font-weight:600"> <br /></span>Run this model online at <a href="http://jjj.biochem.sun.ac.za/">http://jjj.biochem.sun.ac.za</a> <br />To cite JWS Online please refer to: Olivier, B.G. and Snoep, J.L. (2004) <a href="http://bioinformatics.oupjournals.org/cgi/content/abstract/20/13/2143">Web-based modelling using JWS Online</a>, Bioinformatics, 20:2143-2144 </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p align="right"><span style="color:#ffffff">.</span> </p>
<p>This model originates from BioModels Database: A Database of Annotated Published Models. It is copyright (c) 2005-2006 The BioModels Team.</p>
<p>For more information see the <a href="http://www.ebi.ac.uk/biomodels/legal.html">terms of use</a>. </p>
</body></html>
    </Comment>
    <ListOfCompartments>
      <Compartment key="Compartment_0" name="extracellular" simulationType="fixed" dimensionality="3">
      </Compartment>
      <Compartment key="Compartment_1" name="cytosol" simulationType="fixed" dimensionality="3">
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_0" name="Extracellular glucose" simulationType="reactions" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_1" name="Extracellular ethanol" simulationType="reactions" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_2" name="Extracellular glycerol" simulationType="reactions" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_3" name="Extracellular acetaldehyde" simulationType="reactions" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_4" name="Extracellular cyanide" simulationType="reactions" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_5" name="P" simulationType="fixed" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_6" name="Mixed flow cyanide " simulationType="fixed" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_7" name="Mixed flow glucose" simulationType="fixed" compartment="Compartment_0">
      </Metabolite>
      <Metabolite key="Metabolite_8" name="Cytosolic glucose" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_9" name="ATP" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_10" name="Glucose-6-Phosphate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_11" name="ADP" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_12" name="Fructose-6-Phosphate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_13" name="Fructose 1,6-bisphosphate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_14" name="Glyceraldehyde 3-phosphate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_15" name="Dihydroxyacetone phosphate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_16" name="NAD" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_17" name="1,3-Bisphosphoglycerate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_18" name="NADH" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_19" name="Phosphoenolpyruvate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_20" name="Pyruvate" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_21" name="Acetaldehyde" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_22" name="EtOH" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_23" name="Glycerol" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
      <Metabolite key="Metabolite_24" name="AMP" simulationType="reactions" compartment="Compartment_1">
      </Metabolite>
    </ListOfMetabolites>
    <ListOfReactions>
      <Reaction key="Reaction_0" name="Glucose Mixed flow to extracellular medium" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_7" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_0" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1621" name="k0" value="0.048"/>
        </ListOfConstants>
        <KineticLaw function="Function_43">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_258">
              <SourceParameter reference="Metabolite_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_254">
              <SourceParameter reference="Metabolite_7"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_264">
              <SourceParameter reference="Parameter_1621"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1" name="Glucose uptake" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_0" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_8" stoichiometry="59"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_10" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_1620" name="Yvol" value="59"/>
          <Constant key="Parameter_1619" name="K2Glc" value="1.7"/>
          <Constant key="Parameter_1618" name="P2" value="1"/>
          <Constant key="Parameter_1617" name="K2IG6P" value="1.2"/>
          <Constant key="Parameter_1616" name="K2IIG6P" value="7.2"/>
          <Constant key="Parameter_1615" name="Kf" value="1014.96"/>
          <Constant key="Parameter_1614" name="Kr" value="1014.96"/>
          <Constant key="Parameter_1613" name="Kc" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_56">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_335">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_331">
              <SourceParameter reference="Parameter_1615"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_327">
              <SourceParameter reference="Parameter_1620"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_313">
              <SourceParameter reference="Metabolite_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_317">
              <SourceParameter reference="Parameter_1619"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_340">
              <SourceParameter reference="Parameter_1618"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_342">
              <SourceParameter reference="Metabolite_8"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_344">
              <SourceParameter reference="Metabolite_10"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_346">
              <SourceParameter reference="Parameter_1617"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_348">
              <SourceParameter reference="Parameter_1616"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_350">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_352">
              <SourceParameter reference="Parameter_1614"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_339">
              <SourceParameter reference="Parameter_1613"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_2" name="Hexokinase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_8" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_10" stoichiometry="1"/>
          <Product metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1612" name="K3DGlc" value="0.37"/>
          <Constant key="Parameter_1611" name="K3ATP" value="0.1"/>
          <Constant key="Parameter_1610" name="K3Glc" value="0"/>
          <Constant key="Parameter_1609" name="Kc" value="1"/>
          <Constant key="Parameter_1608" name="Km" value="51.7547"/>
        </ListOfConstants>
        <KineticLaw function="Function_57">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_353">
              <SourceParameter reference="Parameter_1609"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_349">
              <SourceParameter reference="Parameter_1608"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_345">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_341">
              <SourceParameter reference="Metabolite_8"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_296">
              <SourceParameter reference="Parameter_1612"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_329">
              <SourceParameter reference="Parameter_1611"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_337">
              <SourceParameter reference="Parameter_1610"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_3" name="Phosphoglucoisomerase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_10" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_12" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1607" name="K4G6P" value="0.8"/>
          <Constant key="Parameter_1606" name="K4F6P" value="0.15"/>
          <Constant key="Parameter_1605" name="K4eq" value="0.13"/>
          <Constant key="Parameter_1604" name="Kc" value="1"/>
          <Constant key="Parameter_1603" name="Kf" value="496.042"/>
          <Constant key="Parameter_1602" name="Kr" value="496.042"/>
        </ListOfConstants>
        <KineticLaw function="Function_53">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_306">
              <SourceParameter reference="Parameter_1604"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_302">
              <SourceParameter reference="Parameter_1603"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_298">
              <SourceParameter reference="Metabolite_10"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_293">
              <SourceParameter reference="Parameter_1607"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_308">
              <SourceParameter reference="Parameter_1606"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_310">
              <SourceParameter reference="Metabolite_12"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_312">
              <SourceParameter reference="Parameter_1602"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_314">
              <SourceParameter reference="Parameter_1605"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_4" name="Phosphofructokinase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_12" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_13" stoichiometry="1"/>
          <Product metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfModifiers>
          <Modifier metabolite="Metabolite_24" stoichiometry="1"/>
        </ListOfModifiers>
        <ListOfConstants>
          <Constant key="Parameter_1601" name="K5" value="0.021"/>
          <Constant key="Parameter_1600" name="kappa5" value="0.15"/>
          <Constant key="Parameter_1599" name="Kc" value="1"/>
          <Constant key="Parameter_1598" name="Km" value="45.4327"/>
        </ListOfConstants>
        <KineticLaw function="Function_58">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_343">
              <SourceParameter reference="Metabolite_12"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_351">
              <SourceParameter reference="Parameter_1601"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_356">
              <SourceParameter reference="Parameter_1600"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_358">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_360">
              <SourceParameter reference="Metabolite_24"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_354">
              <SourceParameter reference="Parameter_1599"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_325">
              <SourceParameter reference="Parameter_1598"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_5" name="Aldolase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_13" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_14" stoichiometry="1"/>
          <Product metabolite="Metabolite_15" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1597" name="K6FBP" value="0.3"/>
          <Constant key="Parameter_1596" name="K6DHAP" value="2"/>
          <Constant key="Parameter_1595" name="K6eq" value="0.081"/>
          <Constant key="Parameter_1594" name="ratio6" value="5"/>
          <Constant key="Parameter_1593" name="K6GAP" value="4"/>
          <Constant key="Parameter_1592" name="K6IGAP" value="10"/>
          <Constant key="Parameter_1591" name="Kc" value="1"/>
          <Constant key="Parameter_1590" name="Kf" value="2207.82"/>
        </ListOfConstants>
        <KineticLaw function="Function_59">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_347">
              <SourceParameter reference="Metabolite_13"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_333">
              <SourceParameter reference="Parameter_1597"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_363">
              <SourceParameter reference="Metabolite_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_365">
              <SourceParameter reference="Parameter_1596"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_367">
              <SourceParameter reference="Parameter_1595"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_369">
              <SourceParameter reference="Parameter_1594"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_371">
              <SourceParameter reference="Metabolite_15"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_373">
              <SourceParameter reference="Parameter_1593"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_375">
              <SourceParameter reference="Parameter_1592"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_361">
              <SourceParameter reference="Parameter_1591"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_357">
              <SourceParameter reference="Parameter_1590"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_6" name="Triosephosphate isomerase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_15" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_14" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1589" name="K7DHAP" value="1.23"/>
          <Constant key="Parameter_1588" name="K7GAP" value="1.27"/>
          <Constant key="Parameter_1587" name="K7eq" value="0.055"/>
          <Constant key="Parameter_1586" name="Kc" value="1"/>
          <Constant key="Parameter_1585" name="Kf" value="116.365"/>
          <Constant key="Parameter_1584" name="Kr" value="116.365"/>
        </ListOfConstants>
        <KineticLaw function="Function_54">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_315">
              <SourceParameter reference="Parameter_1586"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_311">
              <SourceParameter reference="Parameter_1585"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_307">
              <SourceParameter reference="Metabolite_15"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_300">
              <SourceParameter reference="Parameter_1589"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_316">
              <SourceParameter reference="Parameter_1588"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_318">
              <SourceParameter reference="Metabolite_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_320">
              <SourceParameter reference="Parameter_1584"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_322">
              <SourceParameter reference="Parameter_1587"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_7" name="Glyceraldehyde 3-phosphate dehydrogenase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_14" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_16" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_18" stoichiometry="1"/>
          <Product metabolite="Metabolite_17" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1583" name="K8GAP" value="0.6"/>
          <Constant key="Parameter_1582" name="K8NAD" value="0.1"/>
          <Constant key="Parameter_1581" name="K8BPG" value="0.01"/>
          <Constant key="Parameter_1580" name="K8NADH" value="0.06"/>
          <Constant key="Parameter_1579" name="K8eq" value="0.0055"/>
          <Constant key="Parameter_1578" name="Kc" value="1"/>
          <Constant key="Parameter_1577" name="Kf" value="833.858"/>
          <Constant key="Parameter_1576" name="Kr" value="833.858"/>
        </ListOfConstants>
        <KineticLaw function="Function_55">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_323">
              <SourceParameter reference="Parameter_1578"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_304">
              <SourceParameter reference="Metabolite_14"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_309">
              <SourceParameter reference="Metabolite_16"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_324">
              <SourceParameter reference="Parameter_1583"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_326">
              <SourceParameter reference="Parameter_1582"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_328">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_330">
              <SourceParameter reference="Parameter_1581"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_332">
              <SourceParameter reference="Metabolite_18"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_334">
              <SourceParameter reference="Parameter_1580"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_338">
              <SourceParameter reference="Parameter_1579"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_319">
              <SourceParameter reference="Parameter_1577"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_336">
              <SourceParameter reference="Parameter_1576"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_8" name="Phosphoenolpyruvate synthesis" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_17" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_19" stoichiometry="1"/>
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1575" name="Kc" value="1"/>
          <Constant key="Parameter_1574" name="kf" value="443866"/>
          <Constant key="Parameter_1573" name="kr" value="1528.62"/>
        </ListOfConstants>
        <KineticLaw function="Function_52">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_295">
              <SourceParameter reference="Parameter_1575"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="Parameter_1574"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_297">
              <SourceParameter reference="Metabolite_17"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_299">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_301">
              <SourceParameter reference="Parameter_1573"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_303">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_305">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_9" name="Pyruvate kinase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_11" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_19" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_20" stoichiometry="1"/>
          <Product metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1572" name="K10PEP" value="0.2"/>
          <Constant key="Parameter_1571" name="K10ADP" value="0.17"/>
          <Constant key="Parameter_1570" name="Kc" value="1"/>
          <Constant key="Parameter_1569" name="Km" value="343.096"/>
        </ListOfConstants>
        <KineticLaw function="Function_60">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_368">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_364">
              <SourceParameter reference="Metabolite_19"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_321">
              <SourceParameter reference="Parameter_1572"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_359">
              <SourceParameter reference="Parameter_1571"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_376">
              <SourceParameter reference="Parameter_1570"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_372">
              <SourceParameter reference="Parameter_1569"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_10" name="Pyruvate decarboxylase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_20" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1568" name="K11" value="0.3"/>
          <Constant key="Parameter_1567" name="Kc" value="1"/>
          <Constant key="Parameter_1566" name="Km" value="53.1328"/>
        </ListOfConstants>
        <KineticLaw function="Function_61">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_377">
              <SourceParameter reference="Parameter_1567"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_362">
              <SourceParameter reference="Parameter_1566"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_370">
              <SourceParameter reference="Metabolite_20"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_378">
              <SourceParameter reference="Parameter_1568"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_11" name="Alcohol dehydrogenase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_18" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_21" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_16" stoichiometry="1"/>
          <Product metabolite="Metabolite_22" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1565" name="K12NADH" value="0.1"/>
          <Constant key="Parameter_1564" name="K12ACA" value="0.71"/>
          <Constant key="Parameter_1563" name="Kc" value="1"/>
          <Constant key="Parameter_1562" name="Km" value="89.8023"/>
        </ListOfConstants>
        <KineticLaw function="Function_62">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_379">
              <SourceParameter reference="Parameter_1563"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_380">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_382">
              <SourceParameter reference="Metabolite_18"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_384">
              <SourceParameter reference="Parameter_1565"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_386">
              <SourceParameter reference="Parameter_1564"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_366">
              <SourceParameter reference="Parameter_1562"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_12" name="Ethanol out" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_22" stoichiometry="59"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1561" name="k13" value="16.72"/>
          <Constant key="Parameter_1560" name="Yvol" value="59"/>
        </ListOfConstants>
        <KineticLaw function="Function_44">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_269">
              <SourceParameter reference="Metabolite_22"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_273">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_262">
              <SourceParameter reference="Parameter_1560"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_267">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_271">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_265">
              <SourceParameter reference="Parameter_1561"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_13" name="Ethanol flow" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1559" name="k0" value="0.048"/>
        </ListOfConstants>
        <KineticLaw function="Function_45">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_270">
              <SourceParameter reference="Metabolite_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_274">
              <SourceParameter reference="Parameter_1559"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_14" name="Glycerol synthesis" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_15" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_18" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_23" stoichiometry="1"/>
          <Product metabolite="Metabolite_16" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1558" name="K15DHAP" value="25"/>
          <Constant key="Parameter_1557" name="K15INADH" value="0.034"/>
          <Constant key="Parameter_1556" name="K15INAD" value="0.13"/>
          <Constant key="Parameter_1555" name="K15NADH" value="0.13"/>
          <Constant key="Parameter_1554" name="Kc" value="1"/>
          <Constant key="Parameter_1553" name="Km" value="81.4797"/>
        </ListOfConstants>
        <KineticLaw function="Function_63">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_387">
              <SourceParameter reference="Parameter_1554"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_383">
              <SourceParameter reference="Parameter_1553"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_355">
              <SourceParameter reference="Metabolite_15"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_388">
              <SourceParameter reference="Parameter_1558"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_390">
              <SourceParameter reference="Parameter_1557"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_392">
              <SourceParameter reference="Metabolite_18"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_394">
              <SourceParameter reference="Metabolite_16"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_396">
              <SourceParameter reference="Parameter_1556"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_398">
              <SourceParameter reference="Parameter_1555"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_15" name="Glycerol out" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_23" stoichiometry="59"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1552" name="k16" value="1.9"/>
          <Constant key="Parameter_1551" name="Yvol" value="59"/>
        </ListOfConstants>
        <KineticLaw function="Function_46">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_277">
              <SourceParameter reference="Metabolite_23"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_281">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_266">
              <SourceParameter reference="Parameter_1551"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_275">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_279">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_268">
              <SourceParameter reference="Parameter_1552"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_16" name="Glycerol flow" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_2" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1550" name="k0" value="0.048"/>
        </ListOfConstants>
        <KineticLaw function="Function_47">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_278">
              <SourceParameter reference="Metabolite_2"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_282">
              <SourceParameter reference="Parameter_1550"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_17" name="Acetaldehyde out" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_21" stoichiometry="59"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1549" name="k18" value="24.7"/>
          <Constant key="Parameter_1548" name="Yvol" value="59"/>
        </ListOfConstants>
        <KineticLaw function="Function_48">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_285">
              <SourceParameter reference="Metabolite_21"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_289">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_246">
              <SourceParameter reference="Parameter_1548"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_283">
              <SourceParameter reference="Compartment_1"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_287">
              <SourceParameter reference="Compartment_0"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_276">
              <SourceParameter reference="Parameter_1549"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_18" name="Acetaldehyde flow" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1547" name="k0" value="0.048"/>
        </ListOfConstants>
        <KineticLaw function="Function_49">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_286">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_290">
              <SourceParameter reference="Parameter_1547"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_19" name="Cyanide-Acetaldehyde flow" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_4" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_3" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_5" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1546" name="k20" value="0.00283828"/>
        </ListOfConstants>
        <KineticLaw function="Function_50">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_272">
              <SourceParameter reference="Metabolite_3"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_291">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_284">
              <SourceParameter reference="Parameter_1546"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_20" name="Cyanide flow" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_6" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_4" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1545" name="k0" value="0.048"/>
        </ListOfConstants>
        <KineticLaw function="Function_51">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_294">
              <SourceParameter reference="Metabolite_4"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_288">
              <SourceParameter reference="Metabolite_6"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_292">
              <SourceParameter reference="Parameter_1545"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_21" name="Storage" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_10" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1544" name="k22" value="2.25932"/>
          <Constant key="Parameter_1543" name="Kc" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_64">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_399">
              <SourceParameter reference="Parameter_1543"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_395">
              <SourceParameter reference="Parameter_1544"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_391">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_374">
              <SourceParameter reference="Metabolite_10"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_22" name="ATP consumption" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_11" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1542" name="k23" value="3.2076"/>
          <Constant key="Parameter_1541" name="Kc" value="1"/>
        </ListOfConstants>
        <KineticLaw function="Function_65">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_381">
              <SourceParameter reference="Parameter_1541"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_393">
              <SourceParameter reference="Parameter_1542"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_385">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_23" name="Adenylate kinase" reversible="true">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_9" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_24" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_11" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1540" name="Kc" value="1"/>
          <Constant key="Parameter_1539" name="kf" value="432.9"/>
          <Constant key="Parameter_1538" name="kr" value="133.333"/>
        </ListOfConstants>
        <KineticLaw function="Function_52">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_295">
              <SourceParameter reference="Parameter_1540"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_280">
              <SourceParameter reference="Parameter_1539"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_297">
              <SourceParameter reference="Metabolite_9"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_299">
              <SourceParameter reference="Metabolite_24"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_301">
              <SourceParameter reference="Parameter_1538"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_303">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_305">
              <SourceParameter reference="Metabolite_11"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_1"/>
      <StateTemplateVariable objectReference="Metabolite_21"/>
      <StateTemplateVariable objectReference="Metabolite_8"/>
      <StateTemplateVariable objectReference="Metabolite_23"/>
      <StateTemplateVariable objectReference="Metabolite_22"/>
      <StateTemplateVariable objectReference="Metabolite_11"/>
      <StateTemplateVariable objectReference="Metabolite_14"/>
      <StateTemplateVariable objectReference="Metabolite_15"/>
      <StateTemplateVariable objectReference="Metabolite_10"/>
      <StateTemplateVariable objectReference="Metabolite_16"/>
      <StateTemplateVariable objectReference="Metabolite_3"/>
      <StateTemplateVariable objectReference="Metabolite_19"/>
      <StateTemplateVariable objectReference="Metabolite_12"/>
      <StateTemplateVariable objectReference="Metabolite_4"/>
      <StateTemplateVariable objectReference="Metabolite_20"/>
      <StateTemplateVariable objectReference="Metabolite_1"/>
      <StateTemplateVariable objectReference="Metabolite_2"/>
      <StateTemplateVariable objectReference="Metabolite_0"/>
      <StateTemplateVariable objectReference="Metabolite_17"/>
      <StateTemplateVariable objectReference="Metabolite_13"/>
      <StateTemplateVariable objectReference="Metabolite_24"/>
      <StateTemplateVariable objectReference="Metabolite_9"/>
      <StateTemplateVariable objectReference="Metabolite_18"/>
      <StateTemplateVariable objectReference="Metabolite_5"/>
      <StateTemplateVariable objectReference="Metabolite_6"/>
      <StateTemplateVariable objectReference="Metabolite_7"/>
      <StateTemplateVariable objectReference="Compartment_0"/>
      <StateTemplateVariable objectReference="Compartment_1"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 8.921983296495005e+020 3.451132717971001e+020 2.5268905734e+021 1.1585335596285e+022 9.033212250000002e+020 6.925462724999995e+019 1.776531742500002e+021 2.529299430000001e+021 3.914391975000001e+020 7.758686222940001e+020 2.4088566e+019 2.950849335e+020 3.133669506657e+021 5.239263105e+021 9.907265867310002e+021 1.014598355636999e+021 4.034834805000003e+021 1.625978205e+017 2.794273656000001e+021 1.987306695e+020 1.264649715e+021 1.987306695e+020 0 3.372399240000001e+021 1.44531396e+022 1 1 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_12" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_8" target="" append="1"/>
      <Problem>
        <Parameter name="JacobianRequested" type="bool" value="1"/>
        <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
      </Problem>
      <Method name="Enhanced Newton" type="EnhancedNewton">
        <Parameter name="Resolution" type="unsignedFloat" value="1e-009"/>
        <Parameter name="Derivation Factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Use Newton" type="bool" value="1"/>
        <Parameter name="Use Integration" type="bool" value="1"/>
        <Parameter name="Use Back Integration" type="bool" value="1"/>
        <Parameter name="Accept Negative Concentrations" type="bool" value="0"/>
        <Parameter name="Iteration Limit" type="unsignedInteger" value="50"/>
        <Parameter name="Maximum duration for forward integration" type="unsignedFloat" value="1000000000"/>
        <Parameter name="Maximum duration for backward integration" type="unsignedFloat" value="1000000"/>
      </Method>
    </Task>
    <Task key="Task_13" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="200"/>
        <Parameter name="StepSize" type="float" value="5"/>
        <Parameter name="Duration" type="float" value="1000"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="1"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_14" name="Scan" type="scan" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="1"/>
        <ParameterGroup name="ScanItems">
        </ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="1"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_15" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_9" target="" append="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_16" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_10" target="" append="1"/>
      <Problem>
        <Parameter name="Subtask" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <ParameterText name="ObjectiveExpression" type="expression">
          &lt;CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Ethanol flow],Reference=Flux&gt;/&lt;CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Glucose uptake],Reference=Flux&gt;+5*&lt;CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Ethanol flow],Reference=Flux&gt;
        </ParameterText>
        <Parameter name="Maximize" type="bool" value="1"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Glucose uptake],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Hexokinase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Phosphoglucoisomerase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Phosphofructokinase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Aldolase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Triosephosphate isomerase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Glyceraldehyde 3-phosphate dehydrogenase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Phosphoenolpyruvate synthesis],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Pyruvate kinase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Pyruvate decarboxylase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Alcohol dehydrogenase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Glycerol synthesis],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Storage],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[ATP consumption],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
          <ParameterGroup name="OptimizationItem">
            <Parameter name="LowerBound" type="cn" value="0.01"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Hynne2001 Glycolysis,Vector=Reactions[Adenylate kinase],ParameterGroup=Parameters,Parameter=Kc,Reference=Value"/>
            <Parameter name="StartValue" type="float" value="1"/>
            <Parameter name="UpperBound" type="cn" value="11"/>
          </ParameterGroup>
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="ObjectiveFunction" type="key" value=""/>
      </Problem>
      <Method name="Particle Swarm" type="ParticleSwarm">
        <Parameter name="Iteration Limit" type="unsignedInteger" value="1000000"/>
        <Parameter name="Swarm Size" type="unsignedInteger" value="50"/>
        <Parameter name="Std. Deviation" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_17" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_11" target="" append="1"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <ParameterGroup name="Experiment Set">
        </ParameterGroup>
      </Problem>
      <Method name="Evolutionary Programming" type="EvolutionaryProgram">
        <Parameter name="Number of Generations" type="unsignedInteger" value="200"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_18" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_12" target="" append="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_12"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-009"/>
      </Method>
    </Task>
    <Task key="Task_19" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_13" target="" append="1"/>
      <Problem>
        <Parameter name="ExponentNumber" type="unsignedInteger" value="3"/>
        <Parameter name="DivergenceRequested" type="bool" value="1"/>
        <Parameter name="TransientTime" type="float" value="0"/>
      </Problem>
      <Method name="Wolf Method" type="WolfMethod">
        <Parameter name="Orthonormalization Interval" type="unsignedFloat" value="1"/>
        <Parameter name="Overall time" type="unsignedFloat" value="1000"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-012"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_20" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_14" target="" append="1"/>
      <Problem>
        <Parameter name="SubtaskType" type="unsignedInteger" value="1"/>
        <ParameterGroup name="TargetFunctions">
          <Parameter name="SingleObject" type="cn" value=""/>
          <Parameter name="ObjectListType" type="unsignedInteger" value="1"/>
        </ParameterGroup>
        <ParameterGroup name="ListOfVariables">
        </ParameterGroup>
      </Problem>
      <Method name="Sensitivities Method" type="SensitivitiesMethod">
        <Parameter name="Delta factor" type="unsignedFloat" value="1e-006"/>
        <Parameter name="Delta minimum" type="unsignedFloat" value="1e-012"/>
      </Method>
    </Task>
    <Task key="Task_21" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_15" target="" append="1"/>
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
      </Problem>
      <Method name="ILDM (LSODA,Deuflhard)" type="TimeScaleSeparation(ILDM,Deuflhard)">
        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="1e-006"/>
      </Method>
    </Task>
    <Task key="Task_22" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_8" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_9" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_10" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
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
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_11" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
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
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_12" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
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
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_14" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_15" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
          Automatically generated report.
        </body>
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
  </ListOfReports>
  <GUI>
  </GUI>
  <SBMLReference file="Hynne2001_Glycolysis.xml">
    <SBMLMap SBMLid="ACA" COPASIkey="Metabolite_21"/>
    <SBMLMap SBMLid="ACAX" COPASIkey="Metabolite_3"/>
    <SBMLMap SBMLid="ADP" COPASIkey="Metabolite_11"/>
    <SBMLMap SBMLid="AMP" COPASIkey="Metabolite_24"/>
    <SBMLMap SBMLid="ATP" COPASIkey="Metabolite_9"/>
    <SBMLMap SBMLid="BPG" COPASIkey="Metabolite_17"/>
    <SBMLMap SBMLid="CNX" COPASIkey="Metabolite_4"/>
    <SBMLMap SBMLid="CNX0" COPASIkey="Metabolite_6"/>
    <SBMLMap SBMLid="DHAP" COPASIkey="Metabolite_15"/>
    <SBMLMap SBMLid="EtOH" COPASIkey="Metabolite_22"/>
    <SBMLMap SBMLid="EtOHX" COPASIkey="Metabolite_1"/>
    <SBMLMap SBMLid="F6P" COPASIkey="Metabolite_12"/>
    <SBMLMap SBMLid="FBP" COPASIkey="Metabolite_13"/>
    <SBMLMap SBMLid="G6P" COPASIkey="Metabolite_10"/>
    <SBMLMap SBMLid="GAP" COPASIkey="Metabolite_14"/>
    <SBMLMap SBMLid="Glc" COPASIkey="Metabolite_8"/>
    <SBMLMap SBMLid="GlcX" COPASIkey="Metabolite_0"/>
    <SBMLMap SBMLid="GlcX0" COPASIkey="Metabolite_7"/>
    <SBMLMap SBMLid="Glyc" COPASIkey="Metabolite_23"/>
    <SBMLMap SBMLid="GlycX" COPASIkey="Metabolite_2"/>
    <SBMLMap SBMLid="NAD" COPASIkey="Metabolite_16"/>
    <SBMLMap SBMLid="NADH" COPASIkey="Metabolite_18"/>
    <SBMLMap SBMLid="P" COPASIkey="Metabolite_5"/>
    <SBMLMap SBMLid="PEP" COPASIkey="Metabolite_19"/>
    <SBMLMap SBMLid="Pyr" COPASIkey="Metabolite_20"/>
    <SBMLMap SBMLid="cytosol" COPASIkey="Compartment_1"/>
    <SBMLMap SBMLid="extracellular" COPASIkey="Compartment_0"/>
    <SBMLMap SBMLid="vADH" COPASIkey="Reaction_11"/>
    <SBMLMap SBMLid="vAK" COPASIkey="Reaction_23"/>
    <SBMLMap SBMLid="vALD" COPASIkey="Reaction_5"/>
    <SBMLMap SBMLid="vGAPDH" COPASIkey="Reaction_7"/>
    <SBMLMap SBMLid="vGlcTrans" COPASIkey="Reaction_1"/>
    <SBMLMap SBMLid="vHK" COPASIkey="Reaction_2"/>
    <SBMLMap SBMLid="vPDC" COPASIkey="Reaction_10"/>
    <SBMLMap SBMLid="vPFK" COPASIkey="Reaction_4"/>
    <SBMLMap SBMLid="vPGI" COPASIkey="Reaction_3"/>
    <SBMLMap SBMLid="vPK" COPASIkey="Reaction_9"/>
    <SBMLMap SBMLid="vTIM" COPASIkey="Reaction_6"/>
    <SBMLMap SBMLid="vconsum" COPASIkey="Reaction_22"/>
    <SBMLMap SBMLid="vdifACA" COPASIkey="Reaction_17"/>
    <SBMLMap SBMLid="vdifEtOH" COPASIkey="Reaction_12"/>
    <SBMLMap SBMLid="vdifGlyc" COPASIkey="Reaction_15"/>
    <SBMLMap SBMLid="vinCN" COPASIkey="Reaction_20"/>
    <SBMLMap SBMLid="vinGlc" COPASIkey="Reaction_0"/>
    <SBMLMap SBMLid="vlacto" COPASIkey="Reaction_19"/>
    <SBMLMap SBMLid="vlpGlyc" COPASIkey="Reaction_14"/>
    <SBMLMap SBMLid="vlpPEP" COPASIkey="Reaction_8"/>
    <SBMLMap SBMLid="voutACA" COPASIkey="Reaction_18"/>
    <SBMLMap SBMLid="voutEtOH" COPASIkey="Reaction_13"/>
    <SBMLMap SBMLid="voutGlyc" COPASIkey="Reaction_16"/>
    <SBMLMap SBMLid="vstorage" COPASIkey="Reaction_21"/>
  </SBMLReference>
</COPASI>
