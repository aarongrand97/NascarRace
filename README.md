# NascarRace
Car learning to drive around oval track using NEAT algorithm

Having minor issue with pixelation of the track making the search for black pixels in Car.drawDistances occasionally search out of track limits.
Have added a check such that the search isn't performed outside of the window limits to prevent crash. Should be addressed properly if wanting to develop further.
