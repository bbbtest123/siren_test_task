# siren_test_task

Task for test assignment for Middle QA Automation Engineer position at Siren Group

The task:

```
Dear Candidate, 
As the next step of our interview process, we kindly ask you to complete the following task: 

Develop several (at least 3) UI autotests for
https://hb-eta.stage.sirenltd.dev/siding

Use scenario:
-- zip code 09090
-- answer the questions on the form
-- enter the first and last name
-- enter an email
-- enter the phone number
-- (if necessary) confirm the phone number
-- get a "thank you" page.

Feel free to choose the checks yourself.
Use "py test" + "selenium"

Please note that your solution must be in Pull Request (PR) format. 

Please complete the test task within 5 days. Of course, we would appreciate it if you send your solution to the test task earlier. :)

Good luck, and thank you for your interest in our job opportunity! 
```

Task notes:

Implemented the task using pytest+Selenium

Start tests:

```commandline
pytest --browser <browser>
```

where `<browser>` is either `chrome` or `firefox`. Default to `firefox`

Unfortunately, some tests are "flacky", meaning they might pass or fail on different runs. Certainly there is a room for improvements in correctly managed waits.