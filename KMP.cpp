#include "KMP.h"

std::vector<int> kmp (std::string pattern, std::string text){

    if(DEBUG){
        std::cout << "Search for substring " << '"'<< pattern << "\" in string " <<'"'<< text << "\"\n" ;
    }
    //Склеивание образца и текста через символ #, не встречающийся ни в одной из введённых строк
    std::string pattern_text = pattern + "#" + text;
    //Вычисление значения префикс-функции для полученной строки
    std::vector<int> prefix = prefix_func(pattern_text);

    // Инициализация вектора, который будет хранить индексы вхождений образца в текст
    std::vector<int> result;

    if(DEBUG){
        print_tab(1);
        std::cout << "Iteration over the values of the prefix function\n";
    }
    //Итерация по элементам значения префикс-функции
    for (int i = pattern.length() + 1; i < prefix.size(); i++){

        if(DEBUG){
            if(i >= 2*pattern.length()) {
                print_tab(2);
                std::cout << "Current cut: " << text.substr(0, i - pattern.length()) << std::endl;
                print_tab(2);
                print_space(13 + i - 2*pattern.length());
                std::cout << pattern <<"\n";
                if(prefix[i] != pattern.length()){
                    print_tab(3);
                    std::cout << "No match found\n\n";
                }
                else{
                    print_tab(3);
                    std::cout << "Match found at symbol " << i - pattern.length() << " (match starts with symbol "
                    << i -2*pattern.length()<< ")" << "\n\n";
                }
            }
        }
        // Если длина префикс-суффикса равнятеся длине образца, то образец входит в данный текст, а конец вхождения
        // это i-ый символ
        if (prefix[i] == pattern.length()){
            //Запись индекса начала вхождения образца в строку
            result.push_back(i - 2*pattern.length());
        }
    }

    if(result.empty()){
        result.push_back(-1);
    }

    if(DEBUG){
        print_tab(1);
        std::cout << "Answer: [";
        for(int j = 0; j < result.size() - 1; j++){
            std::cout << result[j] << ", ";
        }
        std::cout << result.back() <<"]\n\n";
    }
    return result;
}