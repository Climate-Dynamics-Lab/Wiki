# Archer2

Archer2 is the UK supercomputer, we mainly use it for 
running [CESM2](../climate_models/cesm/index.md) simulations.

To use it, you need to [setup an ARCHER2 account](https://docs.archer2.ac.uk/quick-start/quickstart-users/) and 
then [connect using ssh](https://docs.archer2.ac.uk/user-guide/connecting/).

## Resources
* The Archer2 [documentation](https://docs.archer2.ac.uk/) is good in general.
* [SAFE](https://safe.epcc.ed.ac.uk/): Used to manage account and monitor usage.

## Getting started
To use Archer2, one needs to [obtain a SAFE account](https://docs.archer2.ac.uk/quick-start/quickstart-users/#obtain-an-account-on-the-safe-website),
followed by an [ARCHER2 login account](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-archer2-login-account).

???+ "Login Tip"
    After the first login, to make it easier, I have [config file](https://docs.archer2.ac.uk/user-guide/connecting/#making-access-more-convenient-using-the-ssh-configuration-file) on my 
    local machine at `/Users/user/.ssh/config` with the following (the same file can have
    multiple hosts for different supercomputers):
    ```config
    Host archer2
    HostName login.archer2.ac.uk
    User jamd
    IdentityFile ~/.ssh/id_rsa_archer
    ```

    This means I can just type `ssh archer2` to login directly.

## File Transfer
I find it easiest to transfer files with [globus](https://www.globus.org/data-transfer). Archer2 gives
good [instructions](https://docs.archer2.ac.uk/data-tools/globus/) on how to do this.
