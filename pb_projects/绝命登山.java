import java.util.Random;
public class Main {
    public static void main(String[] args) {
        Random rand = new Random();
        int n = 100;
        int c = 0;
        while (n > 0) {
            n = rand.nextInt(n + 1);
            c += 1;
            System.out.println("第" + c + "天：剩余" + n + "人");
        }
        System.out.println("游戏结束，共存活" + (c - 1) + "天");
        int result = (int) (Math.pow(2, c - 1) - 1) * 10;
        System.out.println("最高收益：+" + result);
    }
}