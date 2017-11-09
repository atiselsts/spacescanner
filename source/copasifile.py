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
# Author: Atis Elsts, 2016-2017
#

from xml.etree import ElementTree

from util import *
import g

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
      </Header>
      <Body>
        <Object cn="CN=Root,Timer=CPU Time"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>

    <Report key="parameterFitting_report" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=CPU time"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Timer=CPU Time"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
  </ListOfReports>
"""


METHOD_SRES = """
      <Method name="Evolution Strategy (SRES)" type="EvolutionaryStrategySR">
        <Parameter name="Number of Generations" type="unsignedInteger" value="1000000"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
        <Parameter name="Pf" type="float" value="0.475"/>
      </Method>"""

METHOD_EP = """
      <Method name="Evolutionary Programming" type="EvolutionaryProgram">
        <Parameter name="Number of Generations" type="unsignedInteger" value="1000000"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>"""

METHOD_GA = """
      <Method name="Genetic Algorithm" type="GeneticAlgorithm">
        <Parameter name="Number of Generations" type="unsignedInteger" value="1000000"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>"""

METHOD_GASR = """
      <Method name="Genetic Algorithm SR" type="GeneticAlgorithmSR">
        <Parameter name="Number of Generations" type="unsignedInteger" value="1000000"/>
        <Parameter name="Population Size" type="unsignedInteger" value="20"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
        <Parameter name="Pf" type="float" value="0.475"/>
      </Method>"""

METHOD_PS = """
      <Method name="Particle Swarm" type="ParticleSwarm">
        <Parameter name="Iteration Limit" type="unsignedInteger" value="1000000"/>
        <Parameter name="Swarm Size" type="unsignedInteger" value="50"/>
        <Parameter name="Std. Deviation" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>"""

METHOD_RS = """
      <Method name="Random Search" type="RandomSearch">
        <Parameter name="Number of Iterations" type="unsignedInteger" value="1000000"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>"""

METHOD_SS = """
      <Method name="Scatter Search" type="ScatterSearch">
        <Parameter name="Number of Iterations" type="unsignedInteger" value="1000000"/>
      </Method>"""

METHOD_SA = """
      <Method name="Simulated Annealing" type="SimulatedAnnealing">
        <Parameter name="Start Temperature" type="unsignedFloat" value="1"/>
        <Parameter name="Cooling Factor" type="unsignedFloat" value="0.85"/>
        <Parameter name="Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>"""

METHOD_SD = """
      <Method name="Steepest Descent" type="SteepestDescent">
        <Parameter name="Iteration Limit" type="unsignedInteger" value="1000"/>
        <Parameter name="Tolerance" type="float" value="1e-06"/>
      </Method>"""

METHOD_TN = """
      <Method name="Truncated Newton" type="TruncatedNewton"></Method>"""


PREDEFINED_METHODS = {
    "ParticleSwarm" : METHOD_PS,
    "ScatterSearch" : METHOD_SS,
    "GeneticAlgorithm" : METHOD_GA,
    "GeneticAlgorithmSR" : METHOD_GASR,
    "EvolutionaryProgram" : METHOD_EP,
    "EvolutionaryStrategySR" : METHOD_SRES,
    "SimulatedAnnealing" : METHOD_SA,
    "RandomSearch" : METHOD_RS,
    "SteepestDescent" : METHOD_SD,
    "TruncatedNewton" : METHOD_TN
}

################################################

class TaskSettings:
    def __init__(self, xmlTask):
        self.xmlTask = xmlTask
        self.paramDict = {}
        self.methodDict = {}
        self.objectiveFunction = None

class CopasiFile:
    def __init__(self, taskType):
        self.taskType = taskType
        self.xmlroot = None
        self.isFileRead = False
        # either optimization or parameter estimation
        self.optimizationTask = None
        self.paramEstimationTask = None
        self.modeFileDirectory = ""

        ElementTree.register_namespace('', COPASI_SCHEMA)

    def read(self, filename):
        self.modeFileDirectory = os.path.dirname(filename)

        if not isReadable(filename):
            s = "error while loading COPASI model: file not found or not readable"
            g.log(LOG_ERROR, s)
            return False, s

        self.isFileRead = True
        self.optimizationTask = None
        self.paramEstimationTask = None

        try:
            self.xmlroot = ElementTree.parse(filename).getroot()
        except:
            self.xmlroot = None
            s = "error while loading COPASI model: failed to parse the XML"
            g.log(LOG_ERROR, s)
            return False, s

        # Example XML structure:
        #   <xml><ListOfTasks><Task type="optimization">...
        for tasklist in self.xmlroot.findall('copasi:ListOfTasks', COPASI_NS):
            for task in tasklist.findall('copasi:Task', COPASI_NS):
                if task.get("type").lower() == "optimization":
                    self.optimizationTask = TaskSettings(task)
                elif task.get("type").lower() == "parameterfitting":
                    self.paramEstimationTask = TaskSettings(task)

        if self.optimizationTask is None and self.paramEstimationTask is None:
            s = "error while loading COPASI model: neither optimization nor parameter estimation tasks found in the COPASI file"
            g.log(LOG_ERROR, s)
            return False, s

        # always load stuff relevant to both optimization and param estimation tasks
        if self.optimizationTask is not None:
            self.loadParameters(self.optimizationTask, "optimizationitem")

            # do validation only if required
            if self.taskType == COPASI_TASK_OPTIMIZATION:
                if len(self.optimizationTask.paramDict) == 0:
                    s = "error while loading COPASI model: parameters for optimization task not defined in the COPASI file"
                    g.log(LOG_ERROR, s)
                    return False, s

                if not self.optimizationTask.objectiveFunction:
                    s = "error while loading COPASI model: objective function not defined in the COPASI file"
                    g.log(LOG_ERROR, s)
                    return False, s

        if self.paramEstimationTask is not None:
            self.loadParameters(self.paramEstimationTask, "fititem")

            # do validation only if required
            if self.taskType == COPASI_TASK_PARAM_ESTIMATION:
                if len(self.paramEstimationTask.paramDict) == 0:
                    s = "error while loading COPASI model: parameters for parameter estimation task not defined in the COPASI file"
                    g.log(LOG_ERROR, s)
                    return False, s

        # return true only if the current state is functional
        return self.isValid(), "loaded ok"


    def loadParameters(self, task, paramGroupName):
        assert task is not None

        problem = task.xmlTask.find('copasi:Problem', COPASI_NS)
        if problem is None:
            g.log(LOG_ERROR, "'Problem' not found in the optimization task")
            return False

        task.paramDict = {}
        task.methodDict = {}

        # Example XML structure:
        #   Task type="optimization"><ParameterGroup name="OptimizationItem"><Parameter> ...
        for paramGroup in problem.findall('copasi:ParameterGroup', COPASI_NS):
            if paramGroup.get("name").lower() == "optimizationitemlist":
                for paramGroup2 in paramGroup.findall('copasi:ParameterGroup', COPASI_NS):

                    if paramGroup2.get("name").lower() != paramGroupName: continue

                    # Example XML syntax:
                    #   <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=Galazzo1990_FermentationPathwayKinetics,Vector=Reactions[Pyruvate kinase],ParameterGroup=Parameters,Parameter=Vm6,Reference=Value"/>
                    for param in paramGroup2.findall('copasi:Parameter', COPASI_NS):

                        if param.get("name").lower() != "objectcn": continue
                        val = param.get("value")
                        #g.log(LOG_ERROR, "param: {} {}".format(param.get("name"), val))
                        if not val: continue
                        val = [x.split("=") for x in  val.split(",")]
                        for (k,v) in val:
                            if 0:
                                if k.lower() == "parameter":
                                    task.paramDict["'" + v + "'"] = paramGroup2
                            else:
                                if k.lower() == "vector":
                                    if "[" in v and "]" in v:
                                        v = v[v.find("[")+1:v.find("]")]
                                    task.paramDict["'" + v + "'"] = paramGroup2

        task.objectiveFunction = None
        for paramText in problem.findall('copasi:ParameterText', COPASI_NS):
           if paramText.get("name").lower() == "objectiveexpression":
               task.objectiveFunction = paramText.text.strip()

        # parse methods as well
        for method in task.xmlTask.findall('copasi:Method', COPASI_NS):
            mtype = method.get("type").lower()
            task.methodDict[mtype] = method

        return True


    def queryParameters(self):
        if not self.isValid():
            return []

        if self.taskType == COPASI_TASK_OPTIMIZATION:
            return list(self.optimizationTask.paramDict.keys())
        if self.taskType == COPASI_TASK_PARAM_ESTIMATION:
            return list(self.paramEstimationTask.paramDict.keys())

        return []


    def writeParam(self, outf, paramName, paramValue, startParamValues, areParametersChangeable):

        if areParametersChangeable:
            if startParamValues is None or paramName not in startParamValues:
                # no need to preprocess; write directly back in the file
                outf.write('          ' + xmlEscapeTabs(ElementTree.tostring(paramValue)))
                return
        else:
            if startParamValues is None:
                startParamValues = {}
            for sub in paramValue.iterfind("*", COPASI_NS):
                if "ParameterGroup" in sub.tag: continue
                if sub.get("name").lower() == "startvalue" and paramName not in startParamValues:
                    # read it directly from the file
                    try:
                        v = sub.get("value")
                        startParamValues[paramName] = float(v)
                    except:
                        g.log(LOG_ERROR, "Getting start value of a parameter " + paramName + " failed:" + sub.get("value"))

        paramGroupName = "OptimizationItem" if self.taskType == "optimization" else "FitItem"
        outf.write(' <ParameterGroup name="{}">\n'.format(paramGroupName))
        for sub in paramValue.iterfind("*", COPASI_NS):
            if "ParameterGroup" in sub.tag: continue

            if sub.get("name").lower() == "startvalue" \
               and startParamValues is not None \
               and paramName in startParamValues:
                # from start values
                val = startParamValues[paramName]
                outf.write('          <Parameter name="StartValue" type="float" value="{}"/>\n'.format(val))
                continue

            if sub.get("name").lower() in ["lowerbound", "upperbound"] \
               and not areParametersChangeable \
               and startParamValues is not None \
               and paramName in startParamValues:
                # unchangeable; set the bounds to the start value
                val = startParamValues[paramName]
                outf.write('          <Parameter name="{}" type="cn" value="{}"/>\n'.format(sub.get("name"), val))
                continue

            # by default, just write back whatever was in the file
            outf.write('          ' + xmlEscapeTabs(ElementTree.tostring(sub)))

        outf.write(' </ParameterGroup>\n')

    def fixupExperimentSet(self, paramGroup):
        for subgroup in paramGroup.iterfind("*", COPASI_NS):
            for elem in subgroup.iterfind("*", COPASI_NS):
                if "type" in elem.attrib and elem.get("type").lower() == "file":
                    # convert relative to absolute path in the same folder where the model resides
                    elem.attrib["value"] = os.path.abspath(
                        os.path.join(self.modeFileDirectory, elem.get("value")))

    def serializeScheduledTask(self, reportFilename, outf, parameters, methodNames,
                               startParamValues, areParametersChangeable):

        taskRef = self.optimizationTask if self.taskType == "optimization" else self.paramEstimationTask

        # Note: 'scheduled' is always set to true to enabled this task when executing from command line.
        # 'update model' is also set to true: to save the final parameter values in the .cps files on which COPASI is run
        outf.write('  <Task key="{}" name="Scheduled Task" type="{}" scheduled="true" updateModel="true">\n'.format(
            taskRef.xmlTask.get("key"), self.taskType))

        # 1. Fix report target file name
        # <Report reference="Report_10" target="./report.log" append="1"/>
        report = taskRef.xmlTask.find('copasi:Report', COPASI_NS)
        if report is not None:
            report.set("target", reportFilename)
            report.set("reference", self.taskType + "_report")
            outf.write('    ' + xmlEscapeTabs(ElementTree.tostring(report)))

        # 2. Include only required parameters
        problem = taskRef.xmlTask.find('copasi:Problem', COPASI_NS)
        outf.write('    <Problem>\n')
        for elem in problem.iterfind("*", COPASI_NS):
            if "Problem" in elem.tag:
                continue

            if "ParameterGroup" in elem.tag:
                if elem.get("name").lower() == "optimizationitemlist":
                    continue # handled separately

                if elem.get("name").lower() == "experiment set":
                    # modify this element to fix the experiment file name
                    self.fixupExperimentSet(elem)

                # just write whatever is there
                outf.write('    ' + xmlEscapeTabs(ElementTree.tostring(elem)))
                continue
    
            if "Parameter" in elem.tag and elem.get("name").lower() == "randomize start values":
                # never randomize them
                outf.write('    <Parameter name="Randomize Start Values" type="bool" value="0"/>\n')
                continue

            # just write whatever is there
            outf.write('    ' + xmlEscapeTabs(ElementTree.tostring(elem)))
            continue


        #print("parameters in the file:", self.paramDict.keys())
        outf.write(' <ParameterGroup name="OptimizationItemList">\n')
        for p in parameters:
            if p in taskRef.paramDict:
                v = taskRef.paramDict[p]
                self.writeParam(outf, p, v, startParamValues, areParametersChangeable)
        outf.write(' </ParameterGroup>\n')
        outf.write(' </Problem>\n')

        # 3. Include only required methods
        #print("methods in the file:", self.methodDict.keys())
        self.serializeMethdods(outf, taskRef, methodNames)

        # finish off
        outf.write('\n  </Task>\n')


    def serializeMethdods(self, outf, taskRef, methodNames):
        for m in methodNames:
            methodFromFile = taskRef.methodDict.get(m.lower())
            if bool(g.getConfig("methodParametersFromFile")) and methodFromFile is not None:
                outf.write('        ' + xmlEscapeTabs(ElementTree.tostring(methodFromFile)))
            else:
                predefinedMethod = PREDEFINED_METHODS.get(m)
                if predefinedMethod is None:
                    g.log(LOG_ERROR, "Unknown or unsupported optimization method {}".format(m))
                else:
                    outf.write('        ' + predefinedMethod)

    def isValid(self):
        if self.taskType == COPASI_TASK_OPTIMIZATION:
            if not self.isFileRead: return True
            if self.optimizationTask is None:
                g.log(LOG_ERROR, "Optimization task not defined in the model file")
                return False
        elif self.taskType == COPASI_TASK_PARAM_ESTIMATION:
            if not self.isFileRead: return True
            if self.paramEstimationTask is None:
                g.log(LOG_ERROR, "Parameter estimation task not defined in the model file")
                return False
        else:
            g.log(LOG_ERROR, "Unknown task type: {}".format(self.taskType))
            return False

        return True


    def createCopy(self, configFilename, reportFilename, parameters, methods,
                   startParamValues, areParametersChangeable):

        if not self.isValid():
            return False

        with open(configFilename, "wt") as outf:
            outf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            outf.write('<!-- generated with SpaceScanner ' + SPACESCANNER_VERSION + ' at ' + getCurrentTime() +' -->\n')
            vmaj = self.xmlroot.get("versionMajor")
            vmin = self.xmlroot.get("versionMinor")
            vdev = self.xmlroot.get("versionDevel")
            outf.write('<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="{}" versionMinor="{}" versionDevel="{}">\n'.format(vmaj, vmin, vdev))
            for elem in self.xmlroot.iterfind("*", COPASI_NS):
                if "ListOfTasks" in elem.tag:
                    outf.write('  <ListOfTasks>\n')
                    for sub in elem.iterfind("*", COPASI_NS):
                        if "ListOfTasks" in sub.tag: continue

                        if (sub == self.optimizationTask.xmlTask and self.taskType == COPASI_TASK_OPTIMIZATION) or \
                           (sub == self.paramEstimationTask.xmlTask and self.taskType == COPASI_TASK_PARAM_ESTIMATION):
                            # This is the scheduled task type, serialize it as such, in a special way
                            self.serializeScheduledTask(reportFilename, outf, parameters, methods,
                                                        startParamValues, areParametersChangeable)
                        else:
                            # This is some other task; make sure it is *not* scheduled
                            # and serialize it in the normal way.
                            sub.attrib["scheduled"] = "false"
                            outf.write('  ' + xmlEscapeTabs(ElementTree.tostring(sub)))

                    outf.write('  </ListOfTasks>\n')
                elif "ListOfReports" in elem.tag:
                    outf.write(REPORT_FORMAT)
                else:
                    outf.write('  ' + xmlEscapeTabs(ElementTree.tostring(elem)))
            outf.write('</COPASI>\n')

        return True

#####################################################
def testOptimizationTask():
    cf = CopasiFile(COPASI_TASK_OPTIMIZATION)
    print("opening a file")
    if not cf.read("../models/complex.cps")[0]:
        return -1
    print("querying parameters")
    params = cf.queryParameters()
    print("parameter names: ", params)
    print("writing a copy")
    cf.createCopy("./input-optimization-task.cps", "./output.log",
                  [params[0], params[-1]], ["ParticleSwarm"],
                  None, True)
    print("all done")

def testParamEstimationTask():
    cf = CopasiFile(COPASI_TASK_PARAM_ESTIMATION)
    print("opening a file")
    if not cf.read("../models/metformin-parameter-estimation.cps")[0]:
        return -1
    print("querying parameters")
    params = cf.queryParameters()
    print("parameter names: ", params)
    print("writing a copy")
    cf.createCopy("./input-param-estimation-task.cps", "./output.log",
                  [params[0], params[-1]], ["ParticleSwarm"],
                  None, True)
    print("all done")

if __name__ == "__main__":
    print("Copasi XML file manager test")
    testOptimizationTask()
    testParamEstimationTask()
