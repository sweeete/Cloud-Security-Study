#include <iostream> // 引入标准输入输出流库，用于控制台输入输出 (cin, cout)
#include <vector>   // 引入动态数组 vector 容器头文件，用于存储股票价格序列

using namespace std; // 使用标准命名空间 std，避免后续频繁书写 std:: 前缀

class solution {
public:
    /**
     * 计算买卖股票能获得的最大利润（贪心算法）
     * @param prices 每天的股票价格数组
     * @return 在允许多次买卖交易下能获得的最大总利润
     */
    int maxprofit(vector<int>& prices) {
        int max_profit=0;      // 初始化累计最大利润变量为 0
        int n = prices.size(); // 获取股票价格数组的总长度（总天数）

        // 从第 2 天（下标为 1）开始遍历到最后一天
        for(int i = 1; i < n; i++) {
            int diff = prices[i] - prices[i - 1]; // 计算当天相对前一天的价格差值
            if(diff > 0) {         // 贪心策略：只要今天价格高于昨天（存在涨幅收益）
                max_profit+=diff;  // 就收集这段正收益，累加到总利润中
            }
        }
        return max_profit; // 返回最终计算出的最大累计利润
    }
};

int main() {
    // 优化 I/O 标准输入输出流性能
    ios_base::sync_with_stdio(false); // 取消 C++ 输入输出流与 C 语言标准流的同步，提升读写效率
    cin.tie(NULL); // 解绑 cin 和 cout，防止每次 cin 输入前自动刷新输出缓冲区

    int n,data;          // 声明变量：n 存储价格天数，data 用于暂存输入的每天价格
    vector<int> prices;  // 声明整型动态数组 prices，用于存放所有天数的股票价格

    if(cin >> n) { // 读取输入的股票价格数组长度 n
        for(int i = 0; i < n; i++){ // 循环 n 次，依次读入每天的价格
            cin>>data;              // 读取单天股票价格
            prices.push_back(data); // 将读取到的价格追加存入 prices 向量末尾
        }

        // 实例化 solution 临时对象并调用 maxprofit 方法计算最大利润
        int res = solution().maxprofit(prices);
        cout<< res; // 输出最终计算出的最大利润值
    }
    return 0; // 程序正常执行完毕，返回状态码 0
}