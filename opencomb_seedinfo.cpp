#include <iostream>
#include <array>
#include <vector>
#include <optional>
#include <random>
#include <algorithm>
#include "json.h"

const std::string image_path_ = "lgtbot://opencomb/resource/";
const uint32_t k_direct_max = 3;
enum class Direct { TOP_LEFT = 0, VERT = 1, TOP_RIGHT = 2};
const std::string style = R"(
<style>
    body {
        margin: 0;
    }
    table {
        margin: 0 auto;
        border-collapse: separate;
        border-spacing: 0;
        border: 1px solid black;
    }
    td {
        font-size: 20px;
        padding: 0;
        border: 1px solid black;
    }
    .white-border {
        text-align:center;
        border: 1px solid white !important;
    }
    .brick {
        position: relative;
        width: 64px;
        height: 64px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .brick img {
        position: absolute;
        width: 100%;
        height: 100%;
        left: 0;
        top: 0;
        z-index: 1;
    }
</style>)";

const std::array<std::vector<int32_t>, k_direct_max> all_points{
    std::vector<int32_t>{3, 4, 8, 10, 0},
    std::vector<int32_t>{1, 5, 9, 10, 0},
    std::vector<int32_t>{2, 6, 7, 10, 0}
};

class AreaCard
{
  public:
    AreaCard() = delete;    // wild card change to 10/10/10

    AreaCard(std::string type) : type_(type) {}

    AreaCard(const int32_t a, const int32_t b, const int32_t c) : points_(std::in_place, std::array<int32_t, k_direct_max>{a, b, c}) {}

    std::string ToHtml(std::string image_path, const bool can_replace = false) const
    {
        std::string div = "<div class='brick'><img src='" + image_path + "card.png'>";
        div += "<img src='" + image_path + ImageName<Direct::VERT>() + ".png'>";
        div += "<img src='" + image_path + ImageName<Direct::TOP_RIGHT>() + ".png'>";
        div += "<img src='" + image_path + ImageName<Direct::TOP_LEFT>() + ".png'>";
        if (can_replace) div += "<img src='" + image_path + "card_replace.png'>";
        div += "</div>";
        return div;
    }

    template <Direct direct>
    std::string ImageName() const
    {
        if (points_.has_value()) {
            int32_t point = points_->at(static_cast<uint32_t>(direct));
            if (point == 10) {
                if (direct == Direct::VERT) return "Xv";
                if (direct == Direct::TOP_LEFT) return "Xl";
                if (direct == Direct::TOP_RIGHT) return "Xr";
            } else if (point == 0) {
                if (direct == Direct::VERT) return "0v";
                if (direct == Direct::TOP_LEFT) return "0l";
                if (direct == Direct::TOP_RIGHT) return "0r";
            } else {
                return std::to_string(point);
            }
        }
        return "";
    }

    std::string Type() const
    {
        if (type_.has_value()) {
            return *type_;
        } else {
            return "";
        }
    }

  private:
    std::optional<std::array<int32_t, k_direct_max>> points_;
    std::optional<std::string> type_;
};

int main() {
    std::string card, seed_str, mode_input, special_input;
    std::string mode = "传统";
    std::string special = "开启";
    std::vector<AreaCard> cards_;
    std::vector<AreaCard> cards2_;

    std::map<std::string, std::any> jsonMap;
    jsonMap["format"] = std::string("markdown");

    if (!(std::cin >> card) || !(std::cin >> seed_str)) {
        jsonMap["format"] = std::string("text");
        jsonMap["content"] = std::string("[参数不足] 格式为：\n#run 开放蜂巢 <模式> <种子> [模式(云顶)] [道具(关闭)]");
        std::cout << json::encodeToJson(jsonMap) << std::endl;
        return 0;
    }
    if (std::cin >> mode_input) {
        if (mode_input == "云顶") {
            mode = "云顶";
        }
    }
    if (std::cin >> special_input) {
        if (special_input == "关闭") {
            special = "关闭";
        }
    }

    // seed
    if (seed_str.empty()) {
        std::random_device rd;
        std::uniform_int_distribution<unsigned long long> dis;
        seed_str = std::to_string(dis(rd));
    }
    std::seed_seq seed(seed_str.begin(), seed_str.end());
    std::mt19937 g(seed);

    // 卡池模板生成
    std::vector<AreaCard> classical_cards_;
    std::vector<AreaCard> wild_cards_;
    std::vector<AreaCard> air_cards_;
    std::vector<AreaCard> chaos_cards_;
    for (const int32_t point_0 : all_points[0]) {
        for (const int32_t point_1 : all_points[1]) {
            for (const int32_t point_2 : all_points[2]) {
                int32_t count0 = (point_0 == 0) + (point_1 == 0) + (point_2 == 0);
                int32_t count10 = (point_0 == 10) + (point_1 == 10) + (point_2 == 10);
                if (count0 == 0 && count10 == 0) {
                    classical_cards_.emplace_back(point_0, point_1, point_2);
                }
                if (count0 == 0 && count10 == 1) {
                    wild_cards_.emplace_back(point_0, point_1, point_2);
                }
                if (count0 == 1 && count10 == 0) {
                    air_cards_.emplace_back(point_0, point_1, point_2);
                }
                if (count0 > 0 && count10 > 0) {
                    chaos_cards_.emplace_back(point_0, point_1, point_2);
                }
            }
        }
    }
    
    if (card == "经典") {
        cards_.insert(cards_.end(), classical_cards_.begin(), classical_cards_.end());
        cards_.insert(cards_.end(), classical_cards_.begin(), classical_cards_.end());
    } else if (card == "癞子") {
        cards_.insert(cards_.end(), classical_cards_.begin(), classical_cards_.end());
        cards_.insert(cards_.end(), wild_cards_.begin(), wild_cards_.end());
    } else if (card == "空气") {
        cards_.insert(cards_.end(), classical_cards_.begin(), classical_cards_.end());
        cards_.insert(cards_.end(), air_cards_.begin(), air_cards_.end());
    } else if (card == "混乱") {
        cards_.insert(cards_.end(), chaos_cards_.begin(), chaos_cards_.end());
        std::shuffle(classical_cards_.begin(), classical_cards_.end(), g);
        std::shuffle(wild_cards_.begin(), wild_cards_.end(), g);
        std::shuffle(air_cards_.begin(), air_cards_.end(), g);
        cards_.insert(cards_.end(), classical_cards_.begin(), classical_cards_.begin() + 10);
        cards_.insert(cards_.end(), wild_cards_.begin(), wild_cards_.begin() + 10);
        cards_.insert(cards_.end(), air_cards_.begin(), air_cards_.begin() + 10);
        cards_.emplace_back(0, 0, 0);
        cards_.emplace_back(0, 0, 0);
    } else {
        jsonMap["format"] = std::string("text");
        jsonMap["content"] = std::string("无效卡池：" + card + "\n仅支持 经典、癞子、空气、混乱");
        std::cout << json::encodeToJson(jsonMap) << std::endl;
        return 0;
    }

    std::vector<AreaCard> tmp_cards = cards_;

    for (uint32_t i = 0; i < 2; ++i) cards_.emplace_back(10, 10, 10);

    if (special == "开启") {
        for (uint32_t i = 0; i < 2; ++i) cards_.emplace_back("wall");
        for (uint32_t i = 0; i < 2; ++i) cards_.emplace_back("wall_broken");
        for (uint32_t i = 0; i < 4; ++i) cards_.emplace_back("erase");
        for (uint32_t i = 0; i < 3; ++i) cards_.emplace_back("move");
        for (uint32_t i = 0; i < 2; ++i) cards_.emplace_back("reshape");
    }

    std::shuffle(cards_.begin(), cards_.end(), g);

    if (special == "开启") {
        // first round
        const std::string special_cards[5] = {"wall", "wall_broken", "erase", "move", "reshape"};
        std::uniform_int_distribution<int32_t> dist(0, 4);
        int32_t start = dist(g);
        cards_.insert(cards_.begin(), special_cards[start]);
    }

    if (mode == "云顶") {
        for (size_t i = 7 + (special == "开启"); i < cards_.size(); i += 7) {
            cards_.insert(cards_.begin() + i, AreaCard("card2"));
        }
        std::shuffle(tmp_cards.begin(), tmp_cards.end(), g);
        cards2_.insert(cards2_.end(), tmp_cards.begin(), tmp_cards.end());
        std::shuffle(tmp_cards.begin(), tmp_cards.end(), g);
        cards2_.insert(cards2_.end(), tmp_cards.begin(), tmp_cards.end());
    }

    // table输出
    std::string table = "<table>";
    table += "<tr><td colspan=5>【卡池】" + card + "</td><td colspan=5>【种子】" + seed_str + "</td></tr>";
    table += "<tr><td colspan=5>【模式】" + mode + "</td><td colspan=5>【道具】" + special + "</td></tr>";
    if (mode == "云顶") table += "<tr><td colspan=10 style='text-align:center;'><b>卡池1</b></td></tr>";

    table += "<tr>";
    int i = 0;
    for (auto card : cards_) {
        table += "<td class='white-border'>";
        if (card.Type() == "") {
            table += card.ToHtml(image_path_);
        } else if (card.Type() == "card2") {
            table += "<b>公共<br>配牌</b>";
        } else {
            table += "<img src='" + image_path_ + card.Type() + ".png'>";
        }
        table += "</td>";
        if (++i % 10 == 0) {
            table += "</tr><tr>";
        }
    }
    table += "</tr>";

    if (mode == "云顶") {
        table += "<tr><td colspan=10 style='text-align:center;'><b>卡池2</b></td></tr>";
        table += "<tr>";
        i = 0;
        for (auto card : cards2_) {
            table += "<td class='white-border'>";
            if (card.Type() == "") {
                table += card.ToHtml(image_path_);
            } else {
                table += "<img src='" + image_path_ + card.Type() + ".png'>";
            }
            table += "</td>";
            if (++i % 10 == 0) {
                table += "</tr><tr>";
            }
        }
        table += "</tr>";
    }

    table += "</table>";
    jsonMap["content"] = style + table;

    std::cout << json::encodeToJson(jsonMap) << std::endl;

    return 0;
}