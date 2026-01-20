# Simulations
This gives information about some specific simulations that have been run.
## CESM2 4xCO2 Simulations

These simulations follow the CDRMIP protocol, where CO2 concentrations are increased at 1% per year from pre-industrials levels (284.3 ppm) until quadrupled (1137.2 ppm), taking 140 years. CO2 concentrations then decrease at 1% per year until they return to their original pre-industrial level, another 140 years. A stabilised CO2 period then follows where CO2 concentrations are kept constant at 284.3 ppm for another 100 years.

The simulations are completed using a fully coupled ocean-atmosphere version of CESM2 with a ~2 degree grid. The simulations are run as hybrid runs branched off from the piControl 2 degree simulations. The 4xCO2 simulations were repeated 6 times for 6 different ensemble members, each branching off from a different start date in the piControl runs. 


#### Atmosphere Model Modifications

The only modifications made to the atmosphere model was the increase/decrease in CO2 concentration. Details listed above.

#### Ocean Model Modifications

An issue was encountered as the simulations approached 4xCO2 and we encountered a CFL condition violation. To resolve this and continue running the simulations the ocean model was made slower by updating dt_count=48, as suggested [here](https://bb.cgd.ucar.edu/cesm/threads/marbl-error.4885/).

#### Ice Model Modifications 

An issue was also encountered in the ice model involving energy conservation. A slight modification was made to the ice model to loosen the energy conservation tolerance, as detailed in step 5 [here](https://bb.cgd.ucar.edu/cesm/threads/faq-cice-thermodynamic-convergence-errors.4202/).


### Output

Due to storage constraints only the first ensemble member has daily and monthly-mean output from both the land and atmosphere models. The remaining 5 ensemble members only have output from the atmosphere model and do not have daily 3D variables.

#### Daily

The following variables are available from the atmosphere model:

_T\*\*, TS, TSMN, TSMX, TREFHT, Q\*\*, QREFHT, Z3\*\*, PS, PRECC, PRECL, U10, U\*\*, V\*\*, LHFLX, SHFLX, SOLIN, FSNT, FSNS, FSDS, FSNTC, FSNSC, FSDSC, FLNT, FLUT, FLNS, FLDS, FLNTC, FLUTC, FLNSC_

The following variables are available from the land model:

_SOILLIQ_

** = only available for the first ensemble member. 

#### Monthly

The following variables are available from the atmosphere model:

_SSAVIS, ADRAIN, ADSNOW, ANRAIN, ANSNOW, AQRAIN, AQSNOW, AREI, AREL, AWNC, AWNI, CCN3, CDNUMC, CLDHGH, CLDICE, CLDLIQ, CLDLOW, CLDMED, CLDTOT, CLOUD, CONCLD, DMS, FICE, FLDS, FLNS, FLNT, FLUT, FREQI, FREQL, FREQR, FREQS, FSDS, FSNS, FSNT, FSNTOA, ICEFRAC, ICWMR, IWC, LHFLX, LWCF, OMEGA, OMEGAT, PBLH, PRECC, PRECL, PRECSC, PRECSL, PS, PSL, Q, QFLX, QRL, QRS, QT, RAINQM, RELHUM, RELVAR, SFDMS, SFSOAG, SHFLX, SNOWQM, SO2, SO2_CLXF, SOLIN, SWCF, T, TAUBLJX, TAUBLJY, TAUGWX, TAUGWY, TAUX, TAUY, TGCLDCWP, TGCLDIWP, TGCLDLWP, TMQ, TREFHT, TS, U, U10, UU, V, VQ, VU, VV, WSUB, Z3_

The following variables are available from the land model:

Standard land model output variables. No modifications were made. 