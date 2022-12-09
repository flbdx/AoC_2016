#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <cassert>

#include <iostream>
#include <fstream>
#include <openssl/md5.h>
#include <deque>
#include <list>
#include <string>
#include <utility>

static inline void md_to_hex(const unsigned char *md, char *out) {
    for (int i = 0; i < 16; i++) {
        *out++ = "0123456789abcdef"[(md[i] >> 4) & 0xF];
        *out++ = "0123456789abcdef"[(md[i] >> 0) & 0xF];
    }
}

static void simple_kdf(const char *salt, unsigned int salt_len, unsigned int idx, char *out) {
    char buffer[64];
    unsigned char md[16];
    memcpy(buffer, salt, salt_len);
    int l = sprintf(buffer + salt_len, "%u", idx);
    MD5(reinterpret_cast<const unsigned char *>(buffer), salt_len + l, md);
    md_to_hex(md, out);
}

static void stretched_kdf(const char *salt, unsigned int salt_len, unsigned int idx, char *out) {
    char buffer[64];
    unsigned char md[16];
    memcpy(buffer, salt, salt_len);
    int l = sprintf(buffer + salt_len, "%u", idx);
    MD5(reinterpret_cast<const unsigned char *>(buffer), salt_len + l, md);
    md_to_hex(md, out);
    for (int i = 0; i < 2016; i++) {
        MD5(reinterpret_cast<const unsigned char *>(out), 32, md);
        md_to_hex(md, out);
    }
}

// let's make this overly complicated for no gain
typedef char md_s[32];
typedef std::pair<md_s, std::list<char> > state;

// get the first char repeated at least 3 times and all 5 same chars sequences
static inline void count(const char *md, std::list<char> &repeats) {
    for (int i = 0; i < 32-2; i++) {
        if (md[i] == md[i+1] && md[i] == md[i+2]) {
            repeats.push_back(md[i]);
            break;
        }
    }
    if (repeats.size() == 0) {
        repeats.push_back(0);
    }
    
    for (int i = 0; i < 32-4; i++) {
        if (md[i] == md[i+1] && md[i] == md[i+2] && md[i] == md[i+3] && md[i] == md[i+4]) {
            repeats.push_back(md[i]);
            i = i+4;
        }
    }
}

template<void(*kdf)(const char *, unsigned int, unsigned int, char *)>
static unsigned int work(const char *salt) {
    unsigned int n_keys = 0;
    unsigned int idx = 0;
    std::deque< state > q;
    int salt_len = (int) strlen(salt);
    
    for (int i = 0; i < 1001; i++) {
        q.emplace_back();
        kdf(salt, salt_len, i, q.back().first);
        count(q.back().first, q.back().second);
    }
    
    auto is_key = [&q, &idx]() -> bool {
        const auto &p = q.front();
        const auto &l = p.second;
        char c = l.front();
        if (c == 0) { // no 3-char sequence
            return false;
        }
        auto it = q.begin();
        ++it;
        for (; it != q.end(); ++it) {
            const auto &l2 = (*it).second;
            auto it2 = l2.begin();
            ++it2;
            for (; it2 != l2.end(); ++it2) {
                if (c == *it2) {
                    return true;
                }
            }
        }
        return false;
    };
    
    while (true) {
        if (is_key()) {
            n_keys += 1;
            if (n_keys == 64) {
                break;
            }
        }
        idx += 1;
        q.pop_front();
        q.emplace_back();
        kdf(salt, salt_len, idx + 1000, q.back().first);
        count(q.back().first, q.back().second);
    }
    return idx;
}

int main() {
    std::ifstream input("input_14");
    if (!input.is_open()) {
        return 1;
    }
    std::string line;
    std::getline(input, line);
    input.close();
    
    assert(work<simple_kdf>("abc") == 22728);
    std::cout << work<simple_kdf>(line.c_str()) << std::endl;
    assert(work<stretched_kdf>("abc") == 22551);
    std::cout << work<stretched_kdf>(line.c_str()) << std::endl;
    return 0;
}
