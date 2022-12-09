#include <cstdlib>
#include <cstdint>
#include <cassert>

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include <openssl/md5.h>

std::string part_1(const std::string door_id) {
    uint64_t i = 0;
    uint8_t md[16] __attribute__((aligned(16)));
    uint32_t *mdtop = reinterpret_cast<uint32_t *>(md);
    std::string pwd;
    while (pwd.size() != 8) {
        std::string s = door_id + std::to_string(i);
        MD5(reinterpret_cast<const uint8_t *>(s.data()), s.size(), md);
        
        if ((*mdtop & 0xf0ffff) == 0) {           
            pwd += "0123456789abcdef"[((*mdtop >> 16) & 0xf)];
        }
        
        i += 1;
    }
    
    return pwd;
}

std::string part_2(const std::string door_id) {
    uint64_t i = 0;
    uint8_t md[16] __attribute__((aligned(16)));
    uint32_t *mdtop = reinterpret_cast<uint32_t *>(md);
    std::vector<char> pwd(8);
    unsigned int l = 0;
    while (l != 8) {
        std::string s = door_id + std::to_string(i);
        MD5(reinterpret_cast<const uint8_t *>(s.data()), s.size(), md);
        
        if ((*mdtop & 0xf0ffff) == 0) {
            unsigned int p = ((*mdtop >> 16) & 0xf);
            if (p < 8 && pwd[p] == 0) {
                pwd[p] = "0123456789abcdef"[((*mdtop >> 28) & 0xf)];
                l ++;
            }
        }
        
        i += 1;
    }
    
    return {pwd.data(), 8};
}

int main() {
    static_assert(__BYTE_ORDER == __LITTLE_ENDIAN, "yup");
    
    std::ifstream input("input_05");
    if (!input.is_open()) {
        return 1;
    }
    std::string line;
    std::getline(input, line);
    input.close();
    
    assert(part_1("abc") == "18f47a30");
    std::cout << part_1(line) << std::endl;
    assert(part_2("abc") == "05ace8e3");
    std::cout << part_2(line) << std::endl;
}
