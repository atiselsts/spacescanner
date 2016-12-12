PYTHON = python
SPACESCANNER = ../source/spacescanner.py

all: test-broken test-fast-consensus test-no-solution test-param-ranges test-param-ranges2 test-solution-timeout test-top test-suspend-resume cleanup

test-fast-consensus:
	@echo Testing a fast consensus...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-fast-consensus.json
	@grep "terminating job 1: consensus reached" spacescanner.log
	@echo ..done
	@echo ""

test-no-solution:
	@echo Testing an infeasible method...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-no-solution.json
	@grep "switching job 1 to a fallback method ParticleSwarm" spacescanner.log
	@grep "terminating job 1" spacescanner.log
	@echo ..done
	@echo ""

test-param-ranges:
	@echo Testing parameter range configuration options...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-param-ranges.json
	@grep "total 18 parameter combination(s) to try out" spacescanner.log
	@grep "starting job 1 (optimization parameters: 'Hexokinase' 'Phosphofructokinase' 'Glucose in')" spacescanner.log
	@grep "terminating job 18" spacescanner.log
	@grep "results of finished jobs saved" spacescanner.log
	@echo ..done
	@echo ""

test-param-ranges2:
	@echo Testing parameter range zero configuration options...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-param-ranges2.json
	@grep "total 0 parameter combination(s) to try out" spacescanner.log
	@grep "starting job 0 (optimization parameters: " spacescanner.log
	@grep "results of finished jobs saved" spacescanner.log
	@echo ..done
	@echo ""

test-solution-timeout:
	@echo Testing behavior on solution timeout...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-solution-timeout.json
	@grep -e "terminating job 1/. (method 'RandomSearch'): CPU time limit exceeded" spacescanner.log
	@echo ..done
	@echo ""

# XXX: this is broken by design now when the new "termination on stagnation" semantics is implemented
test-solution-timeout-allmethods:
	@echo Testing behavior on solution timeout with method switching...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-solution-timeout-allmethods.json
	@grep -e "terminating job 1/. (method 'ParticleSwarm'): CPU time limit exceeded" spacescanner.log
	@grep -e "terminating job 1/. (method 'GeneticAlgorithm'): CPU time limit exceeded" spacescanner.log
	@grep -e "terminating job 1/. (method 'GeneticAlgorithmSR'): CPU time limit exceeded" spacescanner.log
	@grep -e "terminating job 1/. (method 'EvolutionaryStrategySR'): CPU time limit exceeded" spacescanner.log
	@echo ..done
	@echo ""

test-top:
	@echo Testing that the optimization is stopped when an acceptable total optimization potential \(TOP\) value is reached...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-potential-value-reached.json
	@grep -e "good-enough-value criteria reached" spacescanner.log
	@echo ..done
	@echo ""

test-suspend-resume:
	@echo Testing load balancing functionality when there are more jobs than cores...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-suspend-resume.json
	@grep -e "resuming process .*job2/input_job2_runner3.cps" spacescanner.log
	@grep -e "suspending process .*job2/input_job2_runner3.cps" spacescanner.log
	@echo ..done
	@echo ""

test-broken: test-broken-1 test-broken-2 test-broken-3 test-broken-4 test-broken-5 test-broken-6
	@true

test-broken-1:
	@echo Testing broken configurations...
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-broken-bad-parameter.json
	@grep "terminating job 0: failed to evaluate the objective function" spacescanner.log
	@echo ..done
	@echo ""

test-broken-2:
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-broken-no-optimization.json
	@grep "error while loading COPASI model: optimization task not found in COPASI file" spacescanner.log
	@echo ..done
	@echo ""

test-broken-3:
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-broken-no-of.json
	@grep "error while loading COPASI model: objective function not defined in COPASI file" spacescanner.log
	@echo ..done
	@echo ""

test-broken-4:
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-broken-no-parameters.json
	@grep "error while loading COPASI model: optimization parameters not defined in COPASI file" spacescanner.log
	@echo ..done
	@echo ""

test-broken-5:
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-broken-no-file.json
	@grep "error while loading COPASI model: file not found or not readable" spacescanner.log
	@echo ..done
	@echo ""

test-broken-6:
	@rm -f spacescanner.log
	$(PYTHON) $(SPACESCANNER) test-broken-no-such-parameter.json
	@grep "parameter range contains nonexistent parameter name" spacescanner.log
	@echo ..done
	@echo ""

cleanup:
	@echo Cleaning up...
	@rm -f spacescanner.log
