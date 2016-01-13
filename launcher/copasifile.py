# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#  * Redistributions of source code must retain the above copyright notice,
#    this list of  conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#
# Author: Atis Elsts, 2016
#

from xml.etree import ElementTree

from util import *

COPASI_SCHEMA = 'http://www.copasi.org/static/schema'
# XML namespace
COPASI_NS = {'copasi': COPASI_SCHEMA}

REPORT_FORMAT = """\
  <ListOfReports>
    <Report key="optimization_report" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
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
  </ListOfReports>
"""

################################################

def log(level, msg):
    print(msg)

################################################

class CopasiFile:
    def __init__(self):
        self.fileCounter = 0
        self.xmlroot = None
        self.optimizationTask = None
        self.paramDict = {}
        self.methodDict = {}

        ElementTree.register_namespace('', COPASI_SCHEMA)

    def read(self, filename):
        if not isReadable(filename):
            log(LOG_ERROR, "error while loading COPASI model: file not found or not readable")
            return False

        self.optimizationTask = None
        self.xmlroot = ElementTree.parse(filename).getroot()
        # Example XML structure:
        #   <xml><ListOfTasks><Task type="optimization">...
        for tasklist in self.xmlroot.findall('copasi:ListOfTasks', COPASI_NS):
            for task in tasklist.findall('copasi:Task', COPASI_NS):
                if task.get("type").lower() == "optimization":
                    self.optimizationTask = task
        if self.optimizationTask is None:
            log(LOG_ERROR, "error while loading COPASI model: optimization task not found in COPASI file")
            return False

        return True


    def getAllParameters(self):
        assert self.optimizationTask is not None

        problem = self.optimizationTask.find('copasi:Problem', COPASI_NS)
        if problem is None:
            log(LOG_ERROR, "'Problem' not found in the optimization task")
            return []

        self.paramDict = {}
        self.methodDict = {}

        # Example XML structure:
        #   Task type="optimization"><ParameterGroup name="OptimizationItem"><Parameter> ...
        for paramGroup in problem.findall('copasi:ParameterGroup', COPASI_NS):
            if paramGroup.get("name").lower() == "optimizationitemlist":
                for paramGroup2 in paramGroup.findall('copasi:ParameterGroup', COPASI_NS):
                    if paramGroup2.get("name").lower() != "optimizationitem": continue

                    # Example XML syntax:
                    #   <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Pyruvate kinase],ParameterGroup=Parameters,Parameter=Vm6,Reference=Value"/>
                    for param in paramGroup2.findall('copasi:Parameter', COPASI_NS):
                        if param.get("name").lower() != "objectcn": continue
                        val = param.get("value")
                        if not val: continue
                        val = [x.split("=") for x in  val.split(",")]
                        for (k,v) in val:
                            if 0:
                                if k.lower() == "parameter":
                                    self.paramDict[v] = paramGroup2
                            else:
                                if k.lower() == "vector":
                                    if "[" in v and "]" in v:
                                        v = v[v.find("[")+1:v.find("]")]
                                    self.paramDict["'" + v + "'"] = paramGroup2

        # parse methods as well
        for method in self.optimizationTask.findall('copasi:Method', COPASI_NS):
            mtype = method.get("type").lower()
            self.methodDict[mtype] = method

        return self.paramDict.keys()


    def serializeOptimizationTask(self, reportFilename, outf, parameters, methods):
        # start writing
        outf.write('  <Task key="{}" name="Optimization" type="optimization" scheduled="true" updateModel="true">\n'.format(self.optimizationTask.get("key")))

        # 1. Fix report target file name
        # <Report reference="Report_10" target="./report.log" append="1"/>
        report = self.optimizationTask.find('copasi:Report', COPASI_NS)
        if report is not None:
            report.set("target", reportFilename)
            report.set("reference", "optimization_report")
            outf.write('    ' + str(ElementTree.tostring(report)))

        # 2. Include only required parameters
        problem = self.optimizationTask.find('copasi:Problem', COPASI_NS)
        outf.write('    <Problem>\n')
        for elem in problem.iterfind("*", COPASI_NS):
            if "Problem" in elem.tag: continue
            if "ParameterGroup" not in elem.tag or elem.get("name").lower() != "optimizationitemlist":
                outf.write('    ' + str(ElementTree.tostring(elem)))
                continue

        #print("parameters in the file:", self.paramDict.keys())
        outf.write(' <ParameterGroup name="OptimizationItemList">\n')
        for p in parameters:
            if p in self.paramDict:
                outf.write('          ' + str(ElementTree.tostring(self.paramDict[p])))
        outf.write(' </ParameterGroup>\n')
        outf.write(' </Problem>\n')
      
        # 3. Include only required methods
        #print("methods in the file:", self.methodDict.keys())
        for m in methods:
            meth = self.methodDict.get(m.lower())
            if meth is not None:
                outf.write('        ' + str(ElementTree.tostring(meth)))

        # finish off
        outf.write('  </Task>\n')


    def createCopy(self, configFilename, reportFilename, parameters, methods):
        if self.optimizationTask is None:
            return False

        with open(configFilename, "w") as outf:
            outf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            outf.write('<!-- generated with CoRunner ' + CORUNNER_VERSION + ' at ' + getCurrentTime() +' -->\n')
            vmaj = self.xmlroot.get("versionMajor")
            vmin = self.xmlroot.get("versionMinor")
            vdev = self.xmlroot.get("versionDevel")
            outf.write('<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="{}" versionMinor="{}" versionDevel="{}">\n'.format(vmaj, vmin, vdev))
            for elem in self.xmlroot.iterfind("*", COPASI_NS):
                if "ListOfTasks" in elem.tag:
                    outf.write('  <ListOfTasks>\n')
                    for sub in elem.iterfind("*", COPASI_NS):
                        if "ListOfTasks" in sub.tag: continue
                        if sub == self.optimizationTask:
                            self.serializeOptimizationTask(reportFilename, outf, parameters, methods)
                        else:
                            outf.write('  ' + str(ElementTree.tostring(sub)))
                    outf.write('  </ListOfTasks>\n')
                elif "ListOfReports" in elem.tag:
                    outf.write(REPORT_FORMAT)
                else:
                    outf.write('  ' + str(ElementTree.tostring(elem)))
            outf.write('</COPASI>\n')

        return True

#####################################################
def test():
    print("Copasi XML file manager test")
    cf = CopasiFile()
    print("opening a file")
    if not cf.read("/media/atis/sysbio/complex-allparams.cps"):
        return -1
    print("querying parameters")
    params = cf.getAllParameters()
    print("parameter names: ", params)
    print("writing a copy")
    cf.createCopy("./input.cps", "./output.log", [params[0], params[-1]], ["ParticleSwarm"])
    print("all done")

if __name__ == "__main__":
    test()
