# On Github Issues and Pull Requests

Found a bug? Have a new feature to suggest? Want to contribute changes to the codebase? Make sure to read this first.

## Bug reporting

Your code doesn't work, and you have determined that the issue lies with sptm? Follow these steps to report a bug.

1. Search for similar issues. Make sure to delete `is:open` on the issue search to find solved tickets as well. It's possible somebody has encountered this bug already. Still having a problem? Open an issue on Github to let us know.

2. Provide us with a script to reproduce the issue. This script should be runnable as-is and should not require external data download (use randomly generated data if you need to run a model on some test data). We recommend that you use Github Gists to post your code. Any issue that cannot be reproduced is likely to be closed.

3. If possible, take a stab at fixing the bug yourself --if you can!

The more information you provide, the easier it is for us to validate that there is a bug and the faster we'll be able to take action. If you want your issue to be resolved quickly, following the steps above is crucial.

---

## Requesting a Feature

You can also use Github issues to request features you would like to see in sptm, or changes in the sptm API.

1. Provide a clear and detailed explanation of the feature you want and why it's important to add. Keep in mind that the feature should be useful to the majority of users and not just a small subset.

2. Provide code snippets demonstrating the API you have in mind and illustrating the use cases of your feature. Of course, you don't need to write any real code at this point!

3. After discussing the feature you may choose to attempt a Pull Request. If you're at all able, start writing some code. We always have more work to do than time to do it. If you can write some code then that will speed the process along.

---

## Pull Requests

**Where should I submit my pull request?**

1. **sptm improvements and bugfixes** go to the [sptm `master` branch](https://github.com/Rochan-A/sptm/tree/master).

Here's a quick guide to submitting your improvements:

1. If your PR introduces a change in functionality, make sure you start by writing an issue

2. Write the code (or get others to write it). This is the hard part!

3. Make sure any new function or class you introduce has proper docstrings. Make sure any code you touch still has up-to-date docstrings and documentation. **Docstring style should be respected.** In particular, they should be formatted in napolean style (the one followed by Google), and there should be sections for `Args`, `Returns`, `Raises` (if applicable). Look at other docstrings in the codebase for examples.

4. Write tests.

5. When committing, use appropriate, descriptive commit messages.

7. Submit your PR.

---

## Adding new examples

Even if you don't contribute to the sptm source code, if you have an application of sptm that is concise and powerful, please consider adding it to our collection of examples. [Existing examples](https://github.com/Rochan-A/sptm/tree/master/test) show idiomatic sptm code: make sure to keep your own script in the same spirit.
