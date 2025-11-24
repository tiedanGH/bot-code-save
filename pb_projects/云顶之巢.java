import java.util.*;
import java.util.List;
import java.util.Map;

public class Main {

    public boolean ranked = true;

    public List<Piece> pieces = new ArrayList<>();
    public List<Piece> pieces_public = new ArrayList<>();
    public List<Object> players;
    Random rand;
    private int special;
    private boolean test = false;

    private final long seed;
    private static final Map<String, Integer> specialMap = Map.ofEntries(
            Map.entry("1", 1),
            Map.entry("2", 2),
            Map.entry("3", 3),
            Map.entry("4", 4),
            Map.entry("5", 5),
            Map.entry("6", 5),
            Map.entry("7", 5),
            Map.entry("100", 100),
            Map.entry("114514", 114514),
            Map.entry("1919810", 1919810),
            Map.entry("调色盘", 1),
            Map.entry("大的没了", 2),
            Map.entry("大的要来了", 3),
            Map.entry("两极分化", 4),
            Map.entry("有1吗", 5),
            Map.entry("小透不算挂", 6),
            Map.entry("天降恩泽", 7),
            Map.entry("传世经典", 100),
            Map.entry("无9", 2),
            Map.entry("无1", 3),
            Map.entry("无5", 4)
    );
    private final String style = "<style>\n" +
            "    body {\n" +
            "        margin: 0;\n" +
            "    }\n" +
            "    table {\n" +
            "        margin: 0 auto;\n" +
            "        border-collapse: separate;\n" +
            "        border-spacing: 0;\n" +
            "        border: 1px solid black;\n" +
            "    }\n" +
            "    td {\n" +
            "        font-size: 20px;\n" +
            "        padding: 0;\n" +
            "        border: 1px solid black;\n" +
            "    }\n" +
            "    .white-border {\n" +
            "        text-align: center;\n" +
            "        border: 1px solid white !important;\n" +
            "    }\n" +
            "    .brick {\n" +
            "        position: relative;\n" +
            "        width: 64px;\n" +
            "        height: 64px;\n" +
            "        display: flex;\n" +
            "        justify-content: center;\n" +
            "        align-items: center;\n" +
            "    }\n" +
            "    .brick img {\n" +
            "        position: absolute;\n" +
            "        width: 100%;\n" +
            "        height: 100%;\n" +
            "        left: 0;\n" +
            "        top: 0;\n" +
            "        z-index: 1;\n" +
            "    }\n" +
            "</style>";

    public Main(List<Object> players, int special, long seed) {
        this.seed = seed;
        rand = new Random(seed);
        this.players = players;
        this.special = special;
        if (special == 1919810) {
            test = true;
        }
        if (special == 114514) {
            test = true;
            this.special = -1;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int num = 0;
        long seed;
        String special_input = "无";
        try {
            seed = scanner.nextLong();
        } catch (Exception e) {
            System.out.println("[输入错误] 指令格式为：<br>" +
                    "#run 云顶之巢 <种子> [人数] [指定特殊事件]<br>" +
                    "·其中种子和人数只能为数字");
            return;
        }
        if (scanner.hasNextInt()) {
            num = scanner.nextInt();
            if (num < 2 || num > 8) {
                System.out.println("[人数错误] 人数应在 2-8 之间，当前为：" + num + "<br>" +
                        "指令格式为：<br>" +
                        "#run 云顶之巢 <种子> [人数] [指定特殊事件]");
                return;
            }
        }
        if (scanner.hasNext()) {
            special_input = scanner.next();
        }
        scanner.close();
        List<Object> list = new ArrayList<>();
        for (int i = 0; i < num; i++) {
            list.add(null);
        }
        new Main(list, specialMap.getOrDefault(special_input, -1), seed).start();
    }

    public void start() {
        init();
    }


    private void init() {
        int playerSize = players.size();
        special = special == -1 ? rand.nextInt(100) / 12 + 1 : special;
        pieces.clear();
        newPieces(false);
        pieces_public.clear();
        newPieces(true);
        int bound = rand.nextInt(15) + 6;
        for (int i = 0; i < players.size(); i++) {
            if (special == 7) {
                pieces_public.add(0, new Piece(0, 0, 0));
            } else {
                Piece piece = pieces_public.get(i);
                int sum = piece.directions[0] + piece.directions[1] + piece.directions[2];
                if (sum < bound || sum > bound + 4) {
                    int dif = 99;
                    int index = -1;
                    for (int k = players.size(); k < pieces_public.size(); k++) {
                        Piece p1 = pieces_public.get(k);
                        int sum1 = p1.directions[0] + p1.directions[1] + p1.directions[2];
                        if (sum1 >= bound && sum1 <= bound + 4) {
                            pieces_public.set(i, p1);
                            pieces_public.set(k, piece);
                            break;
                        }
                        if (Math.abs(sum1 - bound) < dif) {
                            dif = Math.abs(sum1 - bound);
                            index = k;
                        }
                        if (k == pieces_public.size() - 1) {
                            pieces_public.set(i, pieces_public.get(index));
                            pieces_public.set(index, piece);
                        }
                    }
                }
            }
        }
        // sort the first n(playerSize) pieces in pieces_public by the sum of directions in ascending order
        pieces_public.subList(0, playerSize).sort((o1, o2) -> {
            int sum1 = o1.directions[0] + o1.directions[1] + o1.directions[2];
            int sum2 = o2.directions[0] + o2.directions[1] + o2.directions[2];
            return sum1 - sum2;
        });
        newPieces(true);
        if (special == 1919810) {
            this.pieces_public.clear();
            pieces.clear();
            for (int i = 0; i < 40; i++) {
                pieces.add(new Piece(0, 0, 0));
                this.pieces_public.add(new Piece(0, 0, 0));
            }
        }
        String special_string;
        switch (special) {
            case 1:
                special_string = "本局特殊事件：<b>调色盘</b>——卡池中添加大量癞子";
                break;
            case 2:
                special_string = "本局特殊事件：<b>大的没了</b>——卡池中没有9";
                break;
            case 3:
                special_string = "本局特殊事件：<b>大的要来了</b>——卡池中没有1";
                break;
            case 4:
                special_string = "本局特殊事件：<b>两极分化</b>——卡池中没有5";
                break;
            case 5:
                special_string = "本局特殊事件：<b>有1吗</b>——每行1额外加12分";
                break;
            case 6:
                special_string = "本局特殊事件：<b>小透不算挂</b>——提前公布下一轮的卡（右侧为下一轮）";
                break;
            case 7:
                special_string = "本局特殊事件：<b>天降恩泽</b>——第一轮每人发一个癞子";
                break;
            case 100:
                special_string = "本局特殊事件：<b>传世经典</b>——本局游戏采用传统数字蜂巢规则";
                break;
            default:
                special_string = "本局特殊事件：<b>无</b>";
                break;
        }
        String table = "<table><tr><td colspan=10>【种子】" + seed + "</td></tr>" +
                "<tr><td colspan=10>" + special_string + "</td></tr>" +
                "<tr><td colspan=10 style='text-align:center;'><b>卡池1</b></td></tr>" +
                genHtml(pieces, 1) +
                "<tr><td colspan=10 style='text-align:center;'><b>卡池2</b></td></tr>" +
                genHtml(pieces_public, 2) +
                "</table>";
        System.out.println(style + table);
    }

    private StringBuilder genHtml(List<Piece> pieces, int pool) {
        StringBuilder html = new StringBuilder("<tr>");
        if (pool == 2 && players.isEmpty()) {
            html.append("<td colspan=10 class='white-border'>请输入游戏人数来查看卡池2详情</td></tr>");
            return html;
        }
        int round = 0;
        for (Piece piece : pieces) {
            if (pool == 1) {
                if (round == 0) {
                    html.append("<td class='white-border'><b>开局<br>配牌</b></td>");
                    round++;
                } else if (round % 7 == 0) {
                    html.append("<td class='white-border'><b>公共<br>配牌</b></td>");
                    if (++round % 10 == 0) {
                        html.append("</tr><tr>");
                    }
                }
            }
            html.append("<td class='white-border'>");
            html.append(piece.ToHtml());
            html.append("</td>");
            if (++round % 10 == 0) {
                html.append("</tr><tr>");
            }
        }
        html.append("</tr>");
        return html;
    }

    private void newPieces(boolean inPublic) {
        ArrayList<Piece> pieces = new ArrayList<>();
        for (int i = 0; i < 2; i++) {
            if (special != 3) {
                pieces.add(new Piece(3, 1, 2));
                pieces.add(new Piece(3, 1, 6));
                pieces.add(new Piece(3, 1, 7));
                pieces.add(new Piece(4, 1, 2));
                pieces.add(new Piece(4, 1, 6));
                pieces.add(new Piece(4, 1, 7));
                pieces.add(new Piece(8, 1, 2));
                pieces.add(new Piece(8, 1, 6));
                pieces.add(new Piece(8, 1, 7));
            }
            if (special != 4) {
                pieces.add(new Piece(3, 5, 2));
                pieces.add(new Piece(3, 5, 6));
                pieces.add(new Piece(3, 5, 7));
                pieces.add(new Piece(4, 5, 2));
                pieces.add(new Piece(4, 5, 6));
                pieces.add(new Piece(4, 5, 7));
                pieces.add(new Piece(8, 5, 2));
                pieces.add(new Piece(8, 5, 6));
                pieces.add(new Piece(8, 5, 7));
            }
            if (special != 2) {
                pieces.add(new Piece(3, 9, 2));
                pieces.add(new Piece(3, 9, 6));
                pieces.add(new Piece(3, 9, 7));
                pieces.add(new Piece(4, 9, 2));
                pieces.add(new Piece(4, 9, 6));
                pieces.add(new Piece(4, 9, 7));
                pieces.add(new Piece(8, 9, 2));
                pieces.add(new Piece(8, 9, 6));
                pieces.add(new Piece(8, 9, 7));
            }
            if (!inPublic || special == 1)
                pieces.add(new Piece(0, 0, 0));
        }
        if (inPublic && special == 1) {
            pieces.add(new Piece(0, 0, 0));
        }
        Collections.shuffle(pieces, rand);
        if (!inPublic && special == 1) {
            pieces.add(rand.nextInt(pieces.size()), new Piece(0, 0, 0));
            pieces.add(rand.nextInt(18), new Piece(0, 0, 0));
            pieces.add(rand.nextInt(19), new Piece(0, 0, 0));
        }
        if (!inPublic && special == 100) {
            for (int i = 0; i < 20; i++) {
                if (pieces.get(i).directions[0] == 0) {
                    break;
                }
                if (i == 19) {
                    for (int j = 0; j < 20; j++) {
                        pieces.remove(0);
                    }
                }
            }
        }
        if (inPublic) {
            pieces_public.addAll(pieces);
        } else {
            this.pieces.addAll(pieces);
        }
    }


    public static class Piece {
        int[] directions;
        public final String image_path = "lgtbot://opencomb/resource/";

        public Piece(int dir1, int dir2, int dir3) {
            directions = new int[]{dir1, dir2, dir3};
        }

        public StringBuilder ToHtml() {
            StringBuilder div = new StringBuilder("<div class='brick'><img src='" + image_path + "card.png'>");
            if (directions[0] == 0 && directions[1] == 0 && directions[2] == 0) {
                div.append("<img src='" + image_path).append("Xv.png'>");
                div.append("<img src='" + image_path).append("Xl.png'>");
                div.append("<img src='" + image_path).append("Xr.png'>");
            } else {
                div.append("<img src='" + image_path).append(directions[1]).append(".png'>");
                div.append("<img src='" + image_path).append(directions[2]).append(".png'>");
                div.append("<img src='" + image_path).append(directions[0]).append(".png'>");
            }
            div.append("</div>");
            return div;
        }

        @Override
        public String toString() {
            return directions[0] + " " + directions[1] + " " + directions[2];
        }
    }

}