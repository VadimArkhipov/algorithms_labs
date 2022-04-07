#include "is_cycle.h"

int is_cycle (std::string a, std::string b){

    if(DEBUG){
        std::cout << "Determining if the string \""<< a << "\" is a cyclic shift of the string \"" << b <<"\"\n";
    }

    // Если переданные строки разной длины, то функция возвращает -1, так как в таком случае одна подстрока
    // не может являться циклическим сдвигом другой
    if(a.length() != b.length()){

        if(DEBUG){
            print_tab(1);
            std::cout << "Strings have the different length\n";
        }

        return -1;
    }
    // Вычисляем префикс-функцию для строки, полученной путём склеивания строк через символ #,
    // не встречающийся в строках
    std::vector<int> prefix = prefix_func(b + "#" + a);
    // Рассматриваем последний элемент значения префикс-функции
    // Это значение будет равняться количеству символов суффикса первой строки, которые совпали с префиксом второй строки
    int k = prefix.back();

    if(DEBUG){
        print_tab(1);
        std::cout << "The last value of prefix-function is " << k << std::endl;
        print_tab(1);
        std::cout << "Matching part \"" << a.substr(a.length() - k) << "\"" << std::endl;
        //print_tab(1);
    }
    // Проверка равенства остаточного суффикса второй строки и остаточного префикса первой строки
    // Если рассматриваемые подстроки равны, то одна строка является циклическим сдвигом другой

    if(DEBUG){
        print_tab(2);
        std::cout << "Compare the remain parts: \"" << b.substr(k) << "\" and \"" << a.substr(0, a.length() - k)<< "\"\n";
    }


    if(b.substr(k) == a.substr(0, a.length() - k)){
        //Возвращаем смещени второй строки относительно первой

        if(DEBUG){
            print_tab(2);
            std::cout << "Cuts are equal\n";
        }

        return a.length() - k;
    }

    //Если рассматриваемые подстроки не совпали, то одна строка не является циклическим сдвигом второй
    //Возвращаем -1
    else{
        if(DEBUG){
            print_tab(2);
            std::cout << "Cuts are not equal\n";
        }
        return -1;
    }
}