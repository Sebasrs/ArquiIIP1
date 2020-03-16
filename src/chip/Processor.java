package chip;

public class Processor {
  private Cache L1;
  private int procesorNumber;
  
  public Processor(int procesorNumber) {  
    this.L1 = new Cache();
    this.procesorNumber = procesorNumber;
  }

  public void describeSelf() {
    System.out.println("Procesador " + this.procesorNumber);
  }
}