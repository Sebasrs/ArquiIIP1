package app;

import chip.Chip;

public class Simulation {
  private Chip[] chips = {new Chip(0), new Chip(1)};

  public Simulation(){}

  public void start() {
    for(int i = 0; i < chips.length; i++) {
      chips[i].describeSelf();
    }
  }
}