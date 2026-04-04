class Point2D {
    int x, y;
    public Point2D(int x, int y) {
        this.x = x;
        this.y = y;
    }
    public void offset(int a, int b) {
        x += a;
        y += b;
    }
}
class Point3D extends Point2D {
    int z;
    public Point3D(int x, int y, int z) {
        super(x, y);
        this.z = z;
    }
    public Point3D(Point2D p, int z) {
        super(p.x, p.y);
        this.z = z;
    }
    public void offset(int a, int b, int c) {
        x += a;
        y += b;
        z += c;
    }
    public static void main(String[] args) {
        Point2D p2d1 = new Point2D(1, 2);
        Point2D p2d2 = new Point2D(4, 6);
        double distance2D = Math.sqrt(Math.pow(p2d2.x - p2d1.x, 2) + Math.pow(p2d2.y - p2d1.y, 2));
        System.out.println(distance2D);
        Point3D p3d1 = new Point3D(1, 2, 3);
        Point3D p3d2 = new Point3D(4, 6, 8);
        double distance3D = Math.sqrt(Math.pow(p3d2.x - p3d1.x, 2) +
                Math.pow(p3d2.y - p3d1.y, 2) + Math.pow(p3d2.z - p3d1.z, 2));
        System.out.println(distance3D);
    }
}
