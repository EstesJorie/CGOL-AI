#include "cgol.hpp"
#include <bitset>
#include <set>
#include <unordered_map>

constexpr int WIDTH = 60;
constexpr int HEIGHT = 40;
constexpr int MAX_GENS = 1000;
constexpr int MAX_HISTORY = 10;

using Grid = std::vector<std::vector<bool>>;

struct Hash
{
    size_t operator()(const Grid &grid) const
    {
        size_t hash = 0;
        for (const auto &row : grid)
        {
            for (bool cell : row)
            {
                hash ^= std::hash<bool>()(cell) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
            }
        }
        return hash;
    }
};

Grid createEmptyGrid()
{
    return Grid(HEIGHT, std::vector<bool>(WIDTH, false));
}

Grid wordSeed(const std::string &word)
{
    std::string bitstring;
    for (char c : word)
    {
        std::bitset<8> b(static_cast<unsigned char>(c));
        bitstring += b.to_string();
    }

    Grid grid = createEmptyGrid();
    int startX = (WIDTH - static_cast<int>(bitstring.size())) / 2;
    int startY = HEIGHT / 2;
    if (startX < 0) startX = 0; //stop negative startX

    for(size_t i = 0; i < bitstring.size(); i++)
    {
        grid[startY][startX + static_cast<int>(i)] = (bitstring[i] == '1');
    }

    return grid;
}

int countNeighbours(const Grid &grid, int col, int row)
{
    int count = 0;
    for (int dy = -1; dy <= 1; dy++)
    {
        for (int dx = -1; dx <= 1; dx++)
        {
            if (dy == 0 && dx == 0) continue;
            int newRow = row + dy;
            int newCol = col + dx;
            if (newRow >= 0 && newRow < HEIGHT && newCol >= 0 && newCol < WIDTH)
            {
                count += grid[newRow][newCol];
            }
        }
    }
    return count;
}

Grid nextGeneration(const Grid &grid, int &spawns) {
    Grid newGrid = createEmptyGrid();
    for (int y = 0; y < HEIGHT; ++y) {
        for (int x = 0; x < WIDTH; ++x) {
            int neighbors = countNeighbours(grid, x, y);
            if (grid[y][x]) {
                newGrid[y][x] = (neighbors == 2 || neighbors == 3);
            } else {
                if (neighbors == 3) {
                    newGrid[y][x] = true;
                    spawns++;
                }
            }
        }
    }
    return newGrid;
}

bool isEmpty(const Grid& grid) {
    for (const auto &row : grid) {
        for (bool cell : row) {
            if (cell) return false;
        }
    }
    return true;
}

std::pair<int, int> gameOfLife(const std::string &word) {
    Grid current = wordSeed(word);
    std::vector<Grid> history;
    std::unordered_set<Grid, Hash> seen;

    int generations = 0;
    int score = 0;

    while (generations < MAX_GENS) {
        if (isEmpty(current)) break;

        if (seen.count(current)) {
            break;
        }

        if (history.size() >= MAX_HISTORY) {
            history.erase(history.begin());
        }

        history.push_back(current);
        seen.insert(current);

        int spawns = 0;
        current = nextGeneration(current, spawns);
        score += spawns;
        generations++;
    }
    return {generations, score};
}