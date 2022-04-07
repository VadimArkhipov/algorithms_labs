#include "prefix_func.h"


bool DEBUG = true;

void print_tab(int t){
    while(t > 0) {
        std::cout << "\t";
        t--;
    }
}

void print_space(int s){
    while(s > 0) {
        std::cout << " ";
        s--;
    }
}

// Функция вычисления значения префикс функции
std::vector<int> prefix_func (std::string str){
    // n - длина строки, для которой будет найдено значение префикс-функции
    int n = str.length();

    if(DEBUG){
        print_tab(1);
        std::cout << "Calculation of the prefix function for the string: " << str << std::endl;
        }
    // Инициализация массива, который будет содержать значение префикс-функции. Сейчас он заполнен нулями
    std::vector<int> prefix (n, 0);

    if(DEBUG){
        print_tab(2);
        std::cout << "Current cut: "<< str.substr(0,1) << std::endl;
        print_tab(2);
        std:: cout << "Current length of prefix-suffix for string with right border at 0th symbol: 0\n\n";
    }

    for (int i = 1; i < n; ++i){
        // Значение префикс-функции на предыдущем шаге
        int j = prefix[i-1];
        if(DEBUG){
            print_tab(2);
            std::cout << "Current cut: "<< str.substr(0,1 + i) << std::endl;
            print_tab(2);
            std::cout << "Previous prefix-function value " << j << std::endl;
        }
        // Сравнение символа строки с символом на позиции значения префикс-функции j
        // Если сравниваемые символы не совпадают и значение префикс-функции на предыдущем шаге больше нуля,
        // то значение префикс-функции на данном шаге будет равно значению префикс-функции на предыдущем
        while (j > 0 && str[i] != str[j]){
            if(DEBUG){
                print_tab(2);
                std::cout << "Comparing symbols: " << str[i] << " and " << str[j] << std::endl;
                print_tab(2);
                std::cout << "Symbols are not equal, prefix-function value equals previous\n";
            }
            j = prefix[j-1];
            if(DEBUG){
                print_tab(2);
                std::cout << "prefix-function = " << j << std::endl;
            }
        }
        // Если символы совпали, то значение префикс-функции на данном шаге равняется предыдущему значению
        // увеличенному на единицу
        if (str[i] == str[j]) {
            if(DEBUG){
                print_tab(2);
                std::cout << "Comparing symbols: " << str[i] << " and " << str[j] << std::endl;
                print_tab(2);
                std::cout << "Symbols are equal, increase prefix-function value\n";
            }
            prefix[i] = j + 1;
        }
        else{
            if(DEBUG){
                print_tab(2);
                std::cout << "Comparing symbols: " << str[i] << " and " << str[j] << std::endl;
                print_tab(2);
                std::cout << "Symbols are not equal, prefix-function value still 0\n";
            }
        }

        if(DEBUG){
            print_tab(2);
            std:: cout << "Current length of prefix-suffix for string with right border at " << i << "th symbol: "<< prefix[i] << "\n\n";
        }
    }

    if(DEBUG){
        print_tab(1);
        std::cout << "Prefix-Suffix function value: [";
        for(int j = 0; j < prefix.size() - 1; j++){
            std::cout << prefix[j] << ", ";
        }
        std::cout << prefix.back() <<"]\n\n";
    }
    return prefix;
}

