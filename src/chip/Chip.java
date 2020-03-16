package chip;

public class Chip {
  private Processor[] processors;
  private Cache L2;
  private Controller controller;
  private int chipNumber;

  public Chip(int chipNumber) {
    this.processors = new Processor[2];
    this.processors[0] = new Processor(0);
    this.processors[1] = new Processor(1);
    this.L2 = new Cache();
    this.controller = new Controller();
    this.chipNumber = chipNumber;
  }

  public void describeSelf() {
    System.out.println("chip " + this.chipNumber);
    for(int i = 0; i < processors.length; i++) {
      processors[i].describeSelf();
    }
  }
}