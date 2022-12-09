#include <cstdlib>
#include <cassert>

#include <iostream>
#include <fstream>
#include <string>

static std::string work(const std::string &seed, unsigned int target_len=272) {
    std::string s(seed);
    s.reserve(target_len);
    while (s.size() < target_len) {
        size_t l = s.size();
        s.resize(l * 2 + 1);
        s[l] = '0';
        for (size_t i = 0; i < l; i++) {
            s[l+1+i] = s[l-1-i] == '0' ? '1' : '0';
        }
    }
    
    s.resize(target_len);
    while (true) {
        for (size_t i = 0; i < s.size(); i+=2) {
            s[i/2] = (s[i] == s[i+1]) ? '1' : '0';
        }
        s.resize(s.size() / 2);
        if ((s.size() & 1) != 0) {
            break;
        }
    }
    
    return s;
}

int main() {
    std::ifstream input("input_16");
    if (!input.is_open()) {
        return 1;
    }
    std::string line;
    std::getline(input, line);
    input.close();
    
    assert(work("110010110100", 12) == std::string("100"));
    assert(work("10000", 20) == std::string("01100"));
    std::cout << work(line.c_str()) << std::endl;
    std::cout << work(line.c_str(), 35651584) << std::endl;
    return 0;
}
