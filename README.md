# GLO-4002 E2E Tester

Python E2E Tester for A21 GLO-4002 Project

## Installation

By cloning the repo

```powershell
git clone https://github.com/KerberosMorphy/glo4002-e2e-tester.git
cd glo4002-e2e-tester
pip install .
```

From `pipx`

```powershell
pipx install https://github.com/KerberosMorphy/glo4002-e2e-tester.git
```

From `pip`

```powershell
pip install https://github.com/KerberosMorphy/glo4002-e2e-tester.git
```

Using [PDM](https://pdm.fming.dev/)

```
git clone https://github.com/KerberosMorphy/glo4002-e2e-tester.git
cd glo4002-e2e-tester
pdm install
```

## Usage

Start your server

```powershell
docker build -t application-glo4002 .
docker run -p 8080:8080 -p 8181:8181 application-glo4002
```

Run all tests

```powershell
run-dino-test
```

Run specific tests (as stories 0 and 1)

```powershell
> run-dino-test -s 0 -story 1
 - PASS : test_turn_reset_turn
 - PASS : test_4_turn_1_reset_1_turn
```

List registered tests

```powershell
> run-dino-test --list-stories
Registered Stories
 -  0: test_turn_reset_turn
 -  1: test_4_turn_1_reset_1_turn
 -  2: test_mep2_res_example
```

Help

```powershell
> run-dino-test --help
Usage: run-test [OPTIONS]

Options:
  -s, --story INTEGER  Stories to run
  -l, --list-stories      List Registered Stories
  --help                 Show this message and exit.
```

Using [PDM](https://pdm.fming.dev/)

```powershell
> pdm run run-dino-test
 - PASS : test_turn_reset_turn
 - PASS : test_4_turn_1_reset_1_turn
 - PASS : test_mep2_res_example
 - PASS : test_mep2_dino
 - PASS : test_mep2_res_dino
 - PASS : test_mep2_expiration
 - PASS : test_mep2_w_1_dino
> run-dino-test -s 0 -story 1
 - PASS : test_turn_reset_turn
 - PASS : test_4_turn_1_reset_1_turn
> run-dino-test --list-stories
Registered Stories
 -  0: test_turn_reset_turn
 -  1: test_4_turn_1_reset_1_turn
 -  2: test_mep2_res_example
 -  3: test_mep2_dino
 -  4: test_mep2_res_dino
 -  5: test_mep2_expiration
 -  6: test_mep2_w_1_dino
```

## Add Test

### Add test directly in this project

In `src/dlo4002_e2e_tester/tests.py`, create your test as

```python
def test_turn_reset_turn() -> None:
    get_heartbeat()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    post_reset()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
```

Then register your test at the end of the file

```python
register_test_story_builder(test_story_0)
```

### Add test in your project

```python
from glo4002_e2e_tester.tests import register_test_story_builder
from glo4002_e2e_tester.models import PostTurnResponse
from glo4002_e2e_tester.resources import get_heartbeat, post_turn, post_reset
from glo4002_e2e_tester.tester import main


def my_new_test() -> None:
    get_heartbeat()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    post_reset()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))


register_test_story_builder(my_new_test)


if __name__ == "__main__":
    main()
```

Execute your program

```powershell
> python3 your_program.py --list-stories
Registered Stories
 -  0: test_turn_reset_turn
 -  1: test_4_turn_1_reset_1_turn
 -  2: test_mep2_res_example
 -  3: test_mep2_dino
 -  4: test_mep2_res_dino
 -  5: test_mep2_expiration
 -  6: test_mep2_w_1_dino
 -  7: my_new_test
```

```powershell
> python3 your_program.py --story 7 --story 1
Run tests:
 - FAIL : my_new_test - Invalid status code, 200 != 404
 - PASS : test_4_turn_1_reset_1_turn
```
