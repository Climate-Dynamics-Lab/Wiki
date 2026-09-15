## 1. Log in to Hypatia

Connect to Hypatia using SSH:

```bash
ssh -X <uun>@hypatia.st-andrews.ac.uk
```

Enter your password when prompted.

Create a symbolic link to your shared scratch directory:

```bash
ln -s /sharedscratch/$USER ~/work
```

## 2. Clone CESM2

In your home directory, run:

```bash
cd ~
git clone -b release-cesm2.1.5 https://github.com/ESCOMP/CESM.git my_cesm_sandbox
cd my_cesm_sandbox
./manage_externals/checkout_externals
```

Run the final command twice if necessary.

## 3. Install Conda

Go to the shared Conda directory:

```bash
cd /gpfs01/software/conda/
```

Create a directory using your University username:

```bash
mkdir <uun>
cd <uun>
install-conda
```

Log out of Hypatia and log back in after the installation finishes.

## 4. Set up the Conda environment

The environment only needs to be created once, but it must be activated whenever you use it.

```bash
cd ~/my_cesm_sandbox
conda create -n cesm_36_1 python=3.6 perl
conda activate cesm_36_1
conda install -c bioconda perl-xml-libxml
conda install -c conda-forge esmf
```

## 5. Configure CIME for Hypatia

Create your personal CIME configuration directory:

```bash
mkdir -p ~/.cime
```

Copy the edited configuration files into it:

```bash
cp /sharedscratch/mpb20/for_anna/config_machines.xml ~/.cime/
cp /sharedscratch/mpb20/for_anna/config_compilers.xml ~/.cime/
cp /sharedscratch/mpb20/for_anna/config_batch.xml ~/.cime/
cp /sharedscratch/mpb20/for_anna/setup_for_cesm.sh ~/.cime/
cp /sharedscratch/mpb20/for_anna/xmlcheck.sh ~/.cime/
```

Go to the directory:

```bash
cd ~/.cime
```
