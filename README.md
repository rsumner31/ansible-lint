Ansible-lint
============

ansible-lint checks playbooks for practices and behaviour that could
potentially be improved

Setup
-----
You'll need to add ansible-lint/lib to your PYTHONPATH
```
export PYTHONPATH=$PYTHONPATH:`pwd`/lib
```

Usage
-----

```
Usage: ansible-lint playbook.yml

Options:
  --version     show program's version number and exit
  -h, --help    show this help message and exit
  -L            list all the rules
  -q            quieter, although not silent output
  -r RULESDIR   location of rules directory
  -t TAGS       only check rules tagged with these values
  -T            list all the tags
  -x SKIP_TAGS  only check rules whose tags do not match these values
```

Rules
=====

Rules are described using a class file per rule.
Default rules are named DeprecatedVariableRule.py etc.

Each rule definition should have the following:
* ID: A unique identifier
* Short description: Brief description of the rule
* Description: Behaviour the rule is looking for
* Tags: one or more tags that may be used to include or exclude the rule
* At least of the following methods:
  * ```match``` that takes a line and returns ```None``` or ```False``` if
  the line doesn't match the test and ```True``` or a custom message (this
  allows one rule to test multiple behaviours - see e.g. the
  CommandsInsteadOfModulesRule
  * ```matchblock``` that takes the details about the file and a block.
  It returns ```None``` or ```False``` if the line doesn't match the test
  and ```True``` or a custom message.

An example rule using ```match``` is
```
from ansiblelint import AnsibleLintRule

class DeprecatedVariableRule(AnsibleLintRule):

    id = 'ANSIBLE0001'
    shortdesc = 'Deprecated variable declarations'
    description = 'Check for lines that have old style ${var} ' + \
                  'declarations'
    tags = { 'deprecated' }


    def match(self, line):
        return '${' in line
```

An example rule using ```matchblock``` is
```
import ansiblelint.utils
from ansiblelint import AnsibleLintRule

class TaskHasTag(AnsibleLintRule):
    id = 'ANSIBLE0008'
    shortdesc = 'Tasks must have tag'
    description = 'Tasks must have tag'
    tags = ['productivity']


    def matchblock(self, file, block):
        # The meta files don't have tags
        if file['type'] in ["meta", "playbooks"]:
            return False

        if isinstance(block, basestring):
            return False

        # If the task include another task or make the playbook fail
        # Don't force to have a tag
        if not set(block.keys()).isdisjoint(['include','fail']):
            return False

        # Task should have tags
        if not block.has_key('tags'):
              return True

        return False
```

Examples
--------
There are some example playbooks with undesirable features. Running
ansible-lint on them works:
```
ansible-lint examples/example.yml
[ANSIBLE0006] git used in place of git module
examples/example.yml:31
    action: command git clone blah

[ANSIBLE0002] Trailing whitespace
examples/example.yml:19
    action: do nothing

[ANSIBLE0001] Old style (${var}) brackets
examples/example.yml:10
    action: command echo ${oldskool}

[ANSIBLE0003] Mismatched { and }
examples/example.yml:13
    action: debug oops a missing {{bracket}

[ANSIBLE0004] Checkouts must contain explicit version
examples/example.yml:22
    action: git a=b c=d

[ANSIBLE0004] Checkouts must contain explicit version
examples/example.yml:25
    action: git version=HEAD c=d

[ANSIBLE0004] Checkouts must contain explicit version
examples/example.yml:34
    action: git command

```
If playbooks include other playbooks, or tasks, or handlers or roles, these
are also handled:
```
$ bin/ansible-lint examples/include.yml
[ANSIBLE0003] Mismatched { and }
/Users/will/src/ansible-lint/examples/play.yml:6
    action: oops {{the} bracketing is {{wrong}}

[ANSIBLE0004] Checkouts must contain explicit version
/Users/will/src/ansible-lint/examples/roles/bobbins/tasks/main.yml:3
action: git a=b c=d

```

Contributing
============

Please read CONTRIBUTING.md if you wish to contribute.
