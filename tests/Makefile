PYTHON = python
CORUNNER = ../launcher/corunner.py

all: test-broken test-fast-consensus test-no-solution test-param-ranges test-solution-timeout test-solution-timeout-allmethods test-suspend-resume cleanup

test-fast-consensus:
	@echo Testing a fast consensus...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-fast-consensus.json
	@grep "terminating job 1: consensus reached" corunner.log
	@echo ..done
	@echo ""

test-no-solution:
	@echo Testing an infeasible method...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-no-solution.json
	@grep "switching job 1 to a fallback method ParticleSwarm" corunner.log
	@grep "terminating job 1" corunner.log
	@echo ..done
	@echo ""

test-param-ranges:
	@echo Testing parameter range configuration options...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-param-ranges.json
	@grep "total 18 parameter combination(s) to try out" corunner.log
	@grep "starting job 1 (optimization parameters: 'Hexokinase' 'Phosphofructokinase' 'Glucose in')" corunner.log
	@grep "terminating job 18" corunner.log
	@grep "results of finished jobs saved" corunner.log
	@echo ..done
	@echo ""

test-solution-timeout:
	@echo Testing behavior on solution timeout...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-solution-timeout.json
	@grep -e "terminating job 1/. (method 'RandomSearch'): CPU time limit exceeded" corunner.log
	@echo ..done
	@echo ""

test-solution-timeout-allmethods:
	@echo Testing behavior on solution timeout with method switching...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-solution-timeout-allmethods.json
	@grep -e "terminating job 1/. (method 'ParticleSwarm'): CPU time limit exceeded" corunner.log
	@grep -e "terminating job 1/. (method 'GeneticAlgorithm'): CPU time limit exceeded" corunner.log
	@grep -e "terminating job 1/. (method 'GeneticAlgorithmSR'): CPU time limit exceeded" corunner.log
	@grep -e "terminating job 1/. (method 'EvolutionaryStrategySR'): CPU time limit exceeded" corunner.log
	@echo ..done
	@echo ""

test-suspend-resume:
	@echo Testing load balancing functionality when there are more jobs than cores...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-suspend-resume.json
	@grep -e "resuming process .*job2/input_job2_runner3.cps" corunner.log
	@grep -e "suspending process .*job2/input_job2_runner3.cps" corunner.log
	@echo ..done
	@echo ""

test-broken: test-broken-1 test-broken-2 test-broken-3 test-broken-4 test-broken-5 test-broken-6
	@true

test-broken-1:
	@echo Testing broken configurations...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken-bad-parameter.json
	@grep "terminating job 1: failed to evaluate the objective function" corunner.log
	@echo ..done
	@echo ""

test-broken-2:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken-no-optimization.json
	@grep "error while loading COPASI model: optimization task not found in COPASI file" corunner.log
	@echo ..done
	@echo ""

test-broken-3:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken-no-of.json
	@grep "error while loading COPASI model: objective function not defined in COPASI file" corunner.log
	@echo ..done
	@echo ""

test-broken-4:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken-no-parameters.json
	@grep "error while loading COPASI model: optimization parameters not defined in COPASI file" corunner.log
	@echo ..done
	@echo ""

test-broken-5:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken-no-file.json
	@grep "error while loading COPASI model: file not found or not readable" corunner.log
	@echo ..done
	@echo ""

test-broken-6:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken-no-such-parameter.json
	@grep "parameter range contains nonexistent parameter name" corunner.log
	@echo ..done
	@echo ""

cleanup:
	@echo Cleaning up...
	@rm -f corunner.log
