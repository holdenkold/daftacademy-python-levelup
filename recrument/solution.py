import csv

def count(filename):
    with open(filename, 'r') as input:
        reader = csv.reader(input)
        triangle = list()
        for row in reader:
            triangle.append([int(x) for x in row[0].strip().split(' ')])

        for i in range(len(triangle) -1, 0, -1):
            for j in range(len(triangle[i-1])):
                triangle[i-1][j] += min(triangle[i][j], triangle[i][j+1]) 

        print('Solution for {0}: {1}'.format(filename, triangle[0][0]))


if __name__ == "__main__":
    count('very_easy.txt')
    count('easy.txt')
    count('medium.txt')

