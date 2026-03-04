Random:setSeed = on
Main:timesAllowErrors = 10
Main:numberOfEvents = 1000000 

Next:numberCount = 10000             ! print message every n events

Beams:frameType = 4
Beams:LHEF = /ceph/salshamaily/haa4K_FCCee/madgraph_3.6.6/mg_ee_eeH_HAlpAlp_m6_ecm240/Events/run_01/unweighted_events.lhe

Beams:allowMomentumSpread  = off

!these settings sometimes make the convariant matrix of signals negative and the simulation stops
!they are supposed to be irrelevant for signals anyway

Beams:allowVertexSpread = on
Beams:sigmaVertexX = 5.96E-3
Beams:sigmaVertexY = 23.8E-6
Beams:sigmaVertexZ = 0.397
Beams:sigmaTime = 10.89    !  36.3 ps

PartonLevel:ISR = on
PartonLevel:FSR = on

9000005:all = ALP ALP 0 0 0 60 3.473870e-1 1.0 75.0 0
9000005:oneChannel = 2 1.000 101 321 -321
9000005:mayDecay = on
9000005:isResonance = on
9000005:onMode = off
9000005:onIfAny = 321

LesHouches:setLifetime = 2
