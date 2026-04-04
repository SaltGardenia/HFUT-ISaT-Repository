import java.io.*;
import java.util.*;

public class Inventory {
    private List<InventoryItem/*这是在这个集合中的元素类型，我在后面会有用*/> inventory = new ArrayList<>();
    private List<ShippingRecord> shipping = new ArrayList<>();
    private List<ErrorRecord> errors = new ArrayList<>();

    public static void main(String[] args) {
        Inventory app = new Inventory();
        app.processInventory();
    }

    public void processInventory() {
        readInventory("Inventory.txt");
        processTransactions("Transactions.txt");
        writeShipping("Shipping.txt");
        writeErrors("Errors.txt");
        writeNewInventory("NewInventory.txt");
    }

    // 读取库存文件
    private void readInventory(String filename) {
        try {
            Scanner scanner = new Scanner(new File(filename));
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] parts = line.split("\t");//这一行代码的作用是对于我的内容进行一个分割，使我可以精准的获取我想要获得的内容
                if (parts.length >= 4) {
                    //17	42	6	Widget, blue
                    String itemNumber = parts[0];//17
                    int quantity = Integer.parseInt(parts[1]);//42
                    String supplier = parts[2];//6
                    String description = parts[3];//Widget, blue
                    inventory.add(new InventoryItem(itemNumber, quantity, supplier, description));//可以直接就创建了
                }
            }
            scanner.close();
        } catch (Exception e) {
            e.printStackTrace();
        }//防止异常
    }

    // 处理事务文件
    private void processTransactions(String filename) {
        try {
            Scanner scanner = new Scanner(new File(filename));
            while (scanner.hasNextLine()/*检查是否还有下一行，一直有，一直运行来遍历*/) {
                String line = scanner.nextLine();
                String[] parts = line.split("\t");
                if (parts.length == 0) continue;

                char type = parts[0].charAt(0);//String类的方法，获取字符串中的第某个字符
                switch (type) {//根据任务的不同，分别放入到不同的任务中
                    case 'O':
                        processOrder(parts);
                        break;
                    case 'R':
                        processReceiving(parts);
                        break;
                    case 'A':
                        processAddItem(parts);
                        break;
                    case 'D':
                        processDeleteItem(parts);
                        break;
                }
            }
            scanner.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 处理发货订单
    private void processOrder(String[] parts) {//传入我的内容，因为是O类型
        if (parts.length < 3) return;//用来检测数据够不够，不够就直接返回，不用执行后面的内容了
        String itemNumber = parts[1];
        int quantity = Integer.parseInt(parts[2]);//这个Integer类的作用，就是将字符串转换为整数，强制转化
        String customer = parts.length > 3 ? parts[3] : "Unknown";//对于customer处理

        for (InventoryItem item : inventory) {//这个循环是for-each循环
                                             // 作用是将我集合中的每一个元素取出来赋值给变量
            if (item.getItemNumber().equals(itemNumber)) {//itemNumber是我的传入文件的数据（也就是库存数量），两者相等就直接返回
                //不相等我就要比一比我的库存进行对比，如果大于等于，就直接减掉，如果小于，就直接报错
                if (item.getQuantity() >= quantity) {
                    item.setQuantity(item.getQuantity() - quantity);//改变库存值的大小，存入数据
                    shipping.add(new ShippingRecord(customer, itemNumber, quantity/*这个是我的发货订单，所以我要用quantity*/));//我一开始创建的Shopping集合，来接收
                } else {
                    errors.add(new ErrorRecord(customer, itemNumber, quantity));
                }
                return;
            }
        }
        errors.add(new ErrorRecord(customer, itemNumber, quantity));//压根就没有找到，所以就直接报错
        //因为如果可以查找到，那么就直接返回了，在for循环里就直接退出方法，如果没找到，那么就直接报错。
    }

    // 处理到货单
    private void processReceiving(String[] parts) {
        if (parts.length < 2) return;
        String itemNumber = parts[1];
        int quantity = Integer.parseInt(parts[2]);

        for (InventoryItem item : inventory) {
            if (item.getItemNumber().equals(itemNumber)) {
                item.setQuantity(item.getQuantity() + quantity);//处理，将我的集合中的内容修该
                return;
            }
        }
    }

    // 处理新增货物
    private void processAddItem(String[] parts) {
        if (parts.length < 4) return;
        String itemNumber = parts[1];
        String supplier = parts[2];
        String description = parts[3];

        boolean exists = false;//创建一个布尔类型的变量，用来判断，如果存在，就直接返回，如果不存在，就直接添加
        for (InventoryItem item : inventory) {
            if (item.getItemNumber().equals(itemNumber)) {//对比编号是否有，也就是货物是否存在，如果存在，就直接返回
                exists = true;
                break;
            }
        }
        if (!exists) {//不存在就直接添加，同时假设初始数量为0。
            inventory.add(new InventoryItem(itemNumber, 0, supplier, description));
        }
    }

    // 处理删除货物
    private void processDeleteItem(String[] parts) {
        if (parts.length < 2) return;
        String itemNumber = parts[1];

        for (int i = 0; i < inventory.size(); i++) {
            InventoryItem item = inventory.get(i);//这里的get方法，就是获取集合中的元素，i是索引，就是获得集合中的东西
            //同时记得这里的inventory是我已经在之前做好的记录，所以i是索引，就是获得集合中的东西，是我已经整好的库存。
            //下面这个itemnumber是我的parts[1]，这是我的原来系统的给的库存项
            if (item.getItemNumber().equals(itemNumber)) {//检查当前库存项的货物编号是否与要删除的货物编号匹配。
                if (item.getQuantity() == 0) {//表示如果库存数量为0，就直接删除
                    inventory.remove(i);//直接删除
                } else {//不然就计入错误选项，同时标号为0
                    errors.add(new ErrorRecord("0", itemNumber, item.getQuantity()));
                }
                return;
            }
        }
    }

    // 写入发货记录
    private void writeShipping(String filename) {
        try {
            PrintWriter writer = new PrintWriter(new File(filename));
            for (ShippingRecord record : shipping) {
                writer.println(record.getCustomer() + "\t" + record.getItemNumber() + "\t" + record.getQuantity());
            }//把我要的数据写入到文件中
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 写入错误记录
    private void writeErrors(String filename) {
        try {
            PrintWriter writer = new PrintWriter(new File(filename));
            for (ErrorRecord record : errors) {
                writer.println(record.getCustomer() + "\t" + record.getItemNumber() + "\t" + record.getQuantity());
            }//把错误文件写入
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 写入更新后的库存
    private void writeNewInventory(String filename) {
        try {
            PrintWriter writer = new PrintWriter(new File(filename));
            inventory.sort(Comparator.comparing(InventoryItem::getItemNumber));
            for (InventoryItem item : inventory) {
                writer.println(item.getItemNumber() + "\t" + item.getQuantity() + "\t" + item.getSupplier() + "\t" + item.getDescription());
            }//更新库存文件
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}