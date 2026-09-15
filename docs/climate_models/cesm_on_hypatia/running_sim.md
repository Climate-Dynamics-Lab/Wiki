## 6. Create and run a case

In this example, the case name is `F2000_c4`.

Load the CESM environment:

```bash
source ~/.cime/setup_for_cesm.sh
```

Check the XML configuration:

```bash
bash ~/.cime/xmlcheck.sh
```

Create the case:

```bash
${CIMEROOT}/scripts/create_newcase \
    --case F2000_c4 \
    --compset F2000climo \
    --res f19_f19_mg17 \
    --walltime 00:20:00
```

Enter the case directory:

```bash
cd F2000_c4
```

Set up, build and submit the case:

```bash
./case.setup
./case.build
./case.submit
```

Check the status of your Slurm job:

```bash
squeue -u <uun>
```

## 7. Output and restart files

Archived output is stored in:

```text
~/work/CESM_outputs/archive/
```

Restart files are stored in:

```text
~/work/CESM_outputs/<casename>/run/
```

## 8. Change the simulation length

Run controls, including the simulation length, are stored in the case directory's `env_run.xml` file.

Enter your case directory:

```bash
cd ~/.cime/<casename>
```

For example:

```bash
cd ~/.cime/F2000_c4
```

Check the current value of `STOP_N`:

```bash
./xmlquery STOP_N
```

This returns the number of run units. Check which unit is being used with:

```bash
./xmlquery STOP_OPTION
```

For example, if `STOP_OPTION` is `ndays`, change the simulation length to 10 days with:

```bash
./xmlchange STOP_N=10
```
