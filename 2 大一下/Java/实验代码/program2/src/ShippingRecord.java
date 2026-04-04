class ShippingRecord {
    private String customer;
    private String itemNumber;
    private int quantity;

    public ShippingRecord(String customer, String itemNumber, int quantity) {
        this.customer = customer;
        this.itemNumber = itemNumber;
        this.quantity = quantity;
    }

    public String getCustomer() { return customer; }
    public String getItemNumber() { return itemNumber; }
    public int getQuantity() { return quantity; }

    public void setCustomer(String customer) {
        this.customer = customer;
    }

    public void setItemNumber(String itemNumber) {
        this.itemNumber = itemNumber;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }
}