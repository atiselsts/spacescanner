PYTHON = python2
CORUNNER = ../launcher/corunner.py

all: test-broken test-fast-consensus test-no-solution test-param-ranges test-solution-timeout test-solution-timeout-allmethods cleanup
	@true

test-broken:
	@echo Testing a broken mode file...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken.json
	@grep "terminating job 1: failed to evaluate the objective function" corunner.log
	@grep "terminating job 2: failed to evaluate the objective function" corunner.log
	@echo done
	@echo ""

test-fast-consensus:
	@echo Testing a fast consensus...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-fast-consensus.json
	@grep "terminating job 1: consensus reached" corunner.log
	@echo done
	@echo ""

test-no-solution:
	@echo Testing an infeasible method...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-no-solution.json
	@grep "switching job 1 to a fallback method ParticleSwarm" corunner.log
	@grep "terminating job 1: all fallback methods exhausted without reaching consensus" corunner.log
	@echo done
	@echo ""

test-param-ranges:
	@echo Testing parameter range configuration options...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-param-ranges.json
	@grep "total 18 parameter combination(s) to try out" corunner.log
	@grep "starting job 1 (optimization parameters: 'Hexokinase' 'Phosphofructokinase' 'Glucose in')" corunner.log
	@grep "results of finished jobs saved" corunner.log
	@echo done
	@echo ""

test-solution-timeout:
	@echo Testing behavior on solution timeout...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-solution-timeout.json
	@grep "" corunner.log
	@grep "" corunner.log
	@echo done
	@echo ""

test-solution-timeout-allmethods:
	@echo Testing behavior on solution timeout with method switching...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-solution-timeout-allmethods.json
	@grep "terminating job 1/1 (method 'ParticleSwarm'): CPU time limit exceeded" corunner.log
	@grep "terminating job 1/1 (method 'ParticleSwarm'): CPU time limit exceeded" corunner.log
	@grep "terminating job 1/1 (method 'GeneticAlgorithm'): CPU time limit exceeded" corunner.log
	@grep "terminating job 1/1 (method 'GeneticAlgorithm'): CPU time limit exceeded" corunner.log
	@grep "terminating job 1/1 (method 'GeneticAlgorithmSR'): CPU time limit exceeded" corunner.log
	@grep "terminating job 1/1 (method 'GeneticAlgorithmSR'): CPU time limit exceeded" corunner.log
	@grep "terminating job 1/1 (method 'EvolutionaryStrategySR'): CPU time limit exceeded" corunner.log
	@grep "terminating job 1/1 (method 'EvolutionaryStrategySR'): CPU time limit exceeded" corunner.log
	@echo done
	@echo ""

test-suspend-resume:
	@echo Testing load balancing functionality when there are more jobs than cores...
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-suspend-resume.json
	@grep "resuming process *job2/input_job2_runner3.cps" corunner.log
	@grep "suspending process *job2/input_job2_runner3.cps" corunner.log
	@echo done
	@echo ""

cleanup:
	@echo Cleaning up...
	@rm -f results*
