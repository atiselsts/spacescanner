PYTHON = python2
CORUNNER = ../launcher/corunner.py

all: test-broken test-fast-consensus test-no-solution test-param-ranges test-solution-timeout test-solution-timeout-allmethods cleanup
	@true

test-broken:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-broken.json
	@grep "terminating job 1: failed to evaluate the objective function" corunner.log
	@grep "terminating job 2: failed to evaluate the objective function" corunner.log

test-fast-consensus:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-fast-consensus.json
	@grep "terminating job 1: consensus reached" corunner.log

test-no-solution:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-no-solution.json
	@grep "switching job 1 to a fallback method ParticleSwarm" corunner.log
	@grep "terminating job 1: all fallback methods exhausted without reaching consensus" corunner.log

test-param-ranges:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-param-ranges.json
	@grep "total 18 parameter combination(s) to try out" corunner.log
	@grep "starting job 1 (optimization parameters: 'Hexokinase' 'Phosphofructokinase' 'Glucose in')" corunner.log
	@grep "results of finished jobs saved" corunner.log

test-solution-timeout:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-solution-timeout.json
	@grep "" corunner.log
	@grep "" corunner.log

test-solution-timeout-allmethods:
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

test-suspend-resume:
	@rm -f corunner.log
	$(PYTHON) $(CORUNNER) test-suspend-resume.json
	@grep "resuming process *job2/input_job2_runner3.cps" corunner.log
	@grep "suspending process *job2/input_job2_runner3.cps" corunner.log

cleanup:
	rm -f results*
