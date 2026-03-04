! card adapted from winter23 ww_tautau
Random:setSeed = on
Main:numberOfEvents = 500000         ! number of events to generate
Main:timesAllowErrors = 1000          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 10000             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0          ! print event record n times

Beams:idA = 11                   ! first beam, e+ = 11
Beams:idB = -11                   ! second beam, e- = -11

Beams:allowMomentumSpread  = off

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 2.73e-2   !  27.3 mum
Beams:sigmaVertexY = 48.8E-6   !  48.8 nm
Beams:sigmaVertexZ = 1.33      !  1.33 mm

! 3) Hard process
Beams:eCM = 240  ! CM energy of collision
HiggsSM:ffbar2HZ = on !ZH events

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! no initial-state radiation
PartonLevel:FSR = on               ! no final-state radiation

! Particle decays, turn them off before switching on specific channels
! onIfAll allows more particles to be present
! onIfAny selects all decays where at least one of the particles is present
! onIfMatch selects the specific decay channel, all particles in the list need to match the decay, other particles are not allowed

23:onMode    = off                 ! switch off Z boson decays
23:onIfAny   = 11                   ! switch on Z boson decay to electrons

! Definition of new pseudoscalar
9000006:all = ps psbar 0 0 0 1.5 1.9732e-12 1.0 75.0 0
9000006:oneChannel = 2 1.000 101 321 -321
9000006:mayDecay = on
9000006:isResonance = on
9000006:onMode = off
9000006:onIfAny = 321

! Decay of Higgs boson to  ps psbar
25:onMode = off
25:addChannel = 1 0.000000001 101 9000006 -9000006
25:onIfMatch = 9000006 -9000006
