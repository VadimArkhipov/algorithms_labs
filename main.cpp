#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include "prefix_func.h"
#include "is_cycle.h"
#include "KMP.h"


int main() {
    std::string pattern;
    std::cin >> pattern;
    std::string text;
    std::cin >> text;

// Свдиг
//    int res = is_cycle(pattern, text);
//    if (res == -1){
//        res = is_cycle(text,pattern);
//        if(res != -1){
//            res = pattern.length() - res;
//            }
//        }
//    std::cout << res << std::endl;

 //Поиск образца
    std::vector<int> result = kmp(pattern, text);


    for(int i = 0; i < result.size() - 1; i ++){
        std::cout << result[i] << ",";
    }
    std::cout << result.back() << std::endl;


    return 0;
}
