# JASMIN

JASMIN is the UKs environmental data analysis platform.
The lab stores its [data](../data/index.md) on JASMIN at `/gws/nopw/j04/global_ex`.

## Resources

* Official documentation [🔗](https://help.jasmin.ac.uk/docs/)
* Jupyter notebook service [🔗](https://notebooks.jasmin.ac.uk/)
* List of Scientific Servers [🔗](https://help.jasmin.ac.uk/docs/interactive-computing/sci-servers/)
* [Slurm](slurm.md) Queue information [🔗](https://help.jasmin.ac.uk/docs/batch-computing/slurm-queues/)
* Using Jupyter notebooks on JASMIN without their own service [🔗](https://gist.github.com/bewithankit/1848ba6a4feabd8a750df80b6f3555dc): 
This has the advantage that you can stay within your chosen [IDE](../software/index.md#integrated-development-environment), 
use more memory, and keep working when the notebook service is down.

## Getting started

The [official documentation](https://help.jasmin.ac.uk/docs/getting-started/) is very good for setting up
an account and logging in for the first time.

???+ "Login Tip"
To make the login easier, I have config file on my local machine at `/Users/user/.ssh/config`
(the same file can have multiple hosts for different supercomputers):
```config
Host jasmin
HostName sci-ph-01.jasmin.ac.uk
User jamd1
IdentityFile ~/.ssh/id_rsa_jasmin
ProxyJump login-02.jasmin.ac.uk
```

    This means I can just type `ssh jasmin` to login directly to the sci server in one go.