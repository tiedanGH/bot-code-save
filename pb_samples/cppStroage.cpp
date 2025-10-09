// 导入json.h（此文件会在配置辅助文件为“json.h”时一起上传至glot。源代码请查看：https://pastebin.ubuntu.com/p/BHCGtwXGKr/）
#include "json.h"

using namespace std;

int main() {
    string json_input;
    // 输入第一行存档数据（例如：{"storage":"storage数据","global":"global数据","userID":1145141919810,"nickname":"昵称","from":"测试 群聊(114514)"}）
    getline(cin, json_input);

    // 定义 map<string, any> 用于保存解析后的数据
    map<string, any> data_input;

    // 创建一条jsonSingleMessage图片消息（此处用于输出上次的存储数据）
    map<string, any> singleMessageMap1;

    try {
        // 使用 json::decodeFromString(string) 解析输入字符串至 map<string, any> 格式
        data_input = json::decodeFromString(json_input);
    } catch (const exception& e) {
        cerr << "Error parsing JSON: " << e.what() << endl;
    }


    // 定义一个新的 map<string, any> 用于输出存档数据
    map<string, any> jsonMap;

    // 此处展示的例子为MessageChain格式（消息链）的输出，具体详见帮助文档
    jsonMap["format"] = string("MessageChain");

    // 将旧存档数据保存至 singleMessageMap1 中
    ostringstream contentStream;        // 使用 ostringstream 拼接字符串
    for (const auto& [key, value] : data_input) {
        if (value.type() == typeid(string)) {
        contentStream << key << ": " << any_cast<string>(value) << "\n";
        } else if (value.type() == typeid(long)) {
            contentStream << key << ": " << any_cast<long>(value) << "\n";
        } else {
            contentStream << key << value.type().name() << ": [Unsupported Type]\n";
        }
    }
    singleMessageMap1["content"] = contentStream.str();

    // 简单修改数据至新存储
    // 此处例子为：将存储数据转换为int后+1（需再转换为string）
    try {
        // 提取字符串并转换为整数
        string storage_str = any_cast<string>(data_input["storage"]);
        int storage_value = stoi(storage_str);
        jsonMap["storage"] = to_string(storage_value + 1);
    } catch (const exception& e) {
        jsonMap["storage"] = string("1");
    }
    // 此处例子为：将本次执行代码的用户昵称保存至全局存储(global)
    jsonMap["global"] = data_input["nickname"];

    // 支持嵌套 map（适用于MessageChain和ForwardMessage）
    // 此处例子为：创建一条jsonSingleMessage图片消息
    map<string, any> singleMessageMap2;
    singleMessageMap2["format"] = string("markdown");
    singleMessageMap2["width"] = 300;
    singleMessageMap2["content"] = string("# 消息链图片\n- 测试文本");
    // 此处例子为：创建一条jsonSingleMessage文本消息
    map<string, any> singleMessageMap3;
    singleMessageMap3["content"] = string("测试文字内容");

    // 支持嵌套 vector<any>（适用于MessageChain和ForwardMessage）
    vector<any> messageListVector;
    messageListVector.push_back(singleMessageMap1);
    messageListVector.push_back(singleMessageMap2);
    messageListVector.push_back(singleMessageMap3);
    jsonMap["messageList"] = messageListVector;

    // 使用 json::encodeToJson(map<string, any>) 编码字符串至 JSON 格式
    string json_output = json::encodeToJson(jsonMap);

    // 输出最终JSON字符串
    cout << json_output << endl;
    
    return 0;
}