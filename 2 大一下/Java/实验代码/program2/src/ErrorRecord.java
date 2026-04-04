class ErrorRecord {
    private String customer;
    private String itemNumber;
    private int quantity;

    public ErrorRecord(String customer, String itemNumber, int quantity) {
        this.customer = customer;
        this.itemNumber = itemNumber;
        this.quantity = quantity;
    }

    public String getCustomer() { return customer; }
    public String getItemNumber() { return itemNumber; }
    public int getQuantity() { return quantity; }
}