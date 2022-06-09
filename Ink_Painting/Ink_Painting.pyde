SIZE_RANGE = 800
CONTROL_SIZE_RANGE = 700

FRAME = 0
NUM_FRAMES = 12000

#0 - random, 1 - gaussian, 2 - using range
POSITION_MODE = 0
POSITION_CENTER = PVector(500,500)
RANGE_X = [200, 600]
RANGE_Y = [200, 600]

#0 - random, 1 - from a random color palette, 2 - from a specific color palette, 3 - black, 4 - From Source, 
#5 - Source without Gradient, 6 - Source with Palette, 7 - Source with Palette and not Random, 8
COLOR_MODE = 5
PALETTE = [color(255,196,33), color(138,12,12), color(12,21,138), color(0), color(255)]
# PALETTE = ['#D12229', '#F68A1E', '#FDE01A', '#007940', '#24408E', '#732982']
#PALETTE = ['#0D3B66', '#FAF0CA', '#F4D35E', '#EE964B', '#F95738']

SOURCE_NUM = 25

def setup():
    global POSITION_CENTER, SOURCE_IMG, PALETTE
    size(3000,2000)
    
    if POSITION_MODE == 1:
        POSITION_CENTER = PVector(width/2, height/2)
    
    if COLOR_MODE == 1 or COLOR_MODE == 8:
        numColors = int(random(3, 10))
        PALETTE = []
        for i in range(numColors):
            PALETTE.append(color(random(255), random(255),random(255)))
    
    if COLOR_MODE == 4 or COLOR_MODE == 5 or COLOR_MODE == 6 or COLOR_MODE == 7:
        SOURCE_IMG = loadImage("Source" + str(SOURCE_NUM) + ".png")
        if COLOR_MODE == 6 or COLOR_MODE == 7:
            PALETTE = getAllColors(SOURCE_IMG)
            print(len(PALETTE))
    
def draw():
    global NUM_FRAMES, FRAME, PALETTE
    background(255)
    
    for i in range(NUM_FRAMES):
        (p0, p1, p2, p3) = generatePoints()
        
        minWeight = random(0, 10)
        maxWeight = random(12, 20)
        first = p0
        t = 0.01
        stroke(getColor(p0, p3, 0))
        while t < 1:
            strokeWeight((1-t)*minWeight + t*(maxWeight-minWeight))
            next = getPosition(p0, p1, p2, p3, t)
            line(first.x, first.y, next.x, next.y)
            t += 0.01
            first = next
            if COLOR_MODE == 4:
                stroke(getColor(p0, p3, t))
    
    save(str(FRAME) + ".png")
    # NUM_FRAMES = int(random(50, 150))
    FRAME+=1
    
    if COLOR_MODE == 8:
        numColors = int(random(3, 10))
        PALETTE = []
        for i in range(numColors):
            PALETTE.append(color(random(255), random(255),random(255)))
            
    if FRAME == 120:
        exit()
        
def getColor(p0, p1, t):
    if COLOR_MODE == 0:
        return color(random(255), random(255),random(255))
    elif COLOR_MODE == 1:
        return PALETTE[int(random(len(PALETTE)))]
    elif COLOR_MODE == 2:
        return PALETTE[int(random(len(PALETTE)))]
    elif COLOR_MODE == 3:
        return color(0)
    elif COLOR_MODE == 4:
        x0 = int(p0.x)
        x1 = int(p1.x)
        y0 = int(p0.y)
        y1 = int(p1.y)
        
        x0 = (x0 if x0 < width else width - 1) if x0 > 0 else 0
        x1 = (x1 if x1 < width else width - 1) if x1 > 0 else 0
        y0 = (y0 if y0 < height else height - 1) if y0 > 0 else 0
        y1 = (y1 if y1 < height else height - 1) if y1 > 0 else 0
        
        col0 = SOURCE_IMG.get(x0, y0)
        col1 = SOURCE_IMG.get(x1, y1)
        r = (1-t)*red(col0) + t*red(col1)
        g = (1-t)*green(col0) + t*green(col1)
        b = (1-t)*blue(col0) + t*blue(col1)
        return color(r,g,b)
    elif COLOR_MODE == 5:
        x0 = int(p0.x)
        y0 = int(p0.y)
        
        x0 = (x0 if x0 < width else width - 1) if x0 > 0 else 0
        y0 = (y0 if y0 < height else height - 1) if y0 > 0 else 0
        
        col0 = SOURCE_IMG.get(x0, y0)
        return col0
    elif COLOR_MODE == 6:
        return PALETTE[int(random(len(PALETTE)))]
    elif COLOR_MODE == 7:
        x0 = int(p0.x)
        y0 = int(p0.y)
        
        x0 = (x0 if x0 < width else width - 1) if x0 > 0 else 0
        y0 = (y0 if y0 < height else height - 1) if y0 > 0 else 0
        
        col0 = SOURCE_IMG.get(x0, y0)
        return findClosestColor(col0)
    
    elif COLOR_MODE == 8:
        c = PALETTE[int(random(len(PALETTE)))]
        colorMode(HSB, 360, 100, 100)
        h = hue(c)
        s = saturation(c) + random(-10, 10)
        b = brightness(c) + random(-20, 20)
        newC = color(h,s,b)
        colorMode(RGB, 255)
        return newC
    
def findClosestColor(col):
    avgDiff = 100000000
    closest = 0
    for i in range(len(PALETTE)):
        current = PALETTE[i]
        redDiff = abs(red(current)-red(col))
        greenDiff = abs(green(current) - green(col))
        blueDiff = abs(blue(current) - blue(col))
        newAvg = (redDiff + greenDiff + blueDiff)/3.0
        if newAvg <= avgDiff:
            closest = i
            avgDiff = newAvg
    return PALETTE[closest]
    
def getPosition(p0, p1, p2, p3, t):
    x = (1-t)**3 * p0.x + (1-t)**2 * 3 * t * p1.x + (1-t) * 3 * t**2 * p2.x + t**3 * p3.x
    y = (1-t)**3 * p0.y + (1-t)**2 * 3 * t * p1.y + (1-t) * 3 * t**2 * p2.y + t**3 * p3.y
    next = PVector(x,y)
    return next

def generatePoints():
    if POSITION_MODE == 0:
        p0 = PVector(random(width), random(height))
        p3 = PVector(random(p0.x - SIZE_RANGE, p0.x + SIZE_RANGE), 
                    random(p0.y - SIZE_RANGE, p0.y + SIZE_RANGE))
        p1 = PVector(random(p0.x - CONTROL_SIZE_RANGE, p0.x + CONTROL_SIZE_RANGE), 
                    random(p0.y - CONTROL_SIZE_RANGE, p0.y + CONTROL_SIZE_RANGE))
        p2 = PVector(random(p3.x - CONTROL_SIZE_RANGE, p3.x + CONTROL_SIZE_RANGE), 
                    random(p3.y - CONTROL_SIZE_RANGE, p3.y + CONTROL_SIZE_RANGE))
    elif POSITION_MODE == 1:
        p0 = PVector(skewRandom(0, width, 3), skewRandom(0, height, 3))
        p3 = PVector(random(p0.x - SIZE_RANGE, p0.x + SIZE_RANGE), 
                    random(p0.y - SIZE_RANGE, p0.y + SIZE_RANGE))
        p1 = PVector(random(p0.x - CONTROL_SIZE_RANGE, p0.x + CONTROL_SIZE_RANGE), 
                    random(p0.y - CONTROL_SIZE_RANGE, p0.y + CONTROL_SIZE_RANGE))
        p2 = PVector(random(p3.x - CONTROL_SIZE_RANGE, p3.x + CONTROL_SIZE_RANGE), 
                    random(p3.y - CONTROL_SIZE_RANGE, p3.y + CONTROL_SIZE_RANGE))
    elif POSITION_MODE == 2:
        p0 = PVector(random(RANGE_X[0], RANGE_X[1]), random(RANGE_Y[0], RANGE_Y[1]))
        p3 = PVector(random(p0.x - SIZE_RANGE, p0.x + SIZE_RANGE), 
                    random(p0.y - SIZE_RANGE, p0.y + SIZE_RANGE))
        p1 = PVector(random(p0.x - CONTROL_SIZE_RANGE, p0.x + CONTROL_SIZE_RANGE), 
                    random(p0.y - CONTROL_SIZE_RANGE, p0.y + CONTROL_SIZE_RANGE))
        p2 = PVector(random(p3.x - CONTROL_SIZE_RANGE, p3.x + CONTROL_SIZE_RANGE), 
                    random(p3.y - CONTROL_SIZE_RANGE, p3.y + CONTROL_SIZE_RANGE))
    return (p0, p1, p2, p3)

def skewRandom(minVal, maxVal, amount):
    middle = (maxVal - minVal)/2.0
    bottom = 0
    top = minVal - maxVal
    
    t1 = random(1)**amount
    t2 = random(1)**(1.0/amount)
    
    val1 = (1-t1)*bottom + t1*middle
    val2 = (1-t2)*bottom + t2*middle
    
    avg = val1 + val2
    
    
    gauss = randomGaussian()
    
    sd = (maxVal - minVal)/2.0
    mean = sd + minVal
    
    num = (gauss*sd) + mean
    return avg + minVal

def getAllColors(img):
    colors = []
    for x in range(img.width):
        for y in range(img.height):
            newColor = img.get(x,y)
            colors.append(newColor)
    
    minPixels = 1000
    colors = groupColors(colors)
    return colors
    
# def grouper(iterable):
#     prev = None
#     group = []
#     for item in iterable:
#         if prev is None or item - prev <= 10000:
#             group.append(item)
#         else:
#             yield group
#             group = [item]
#         prev = item
#     if group:
#         yield group


class ColorGroup:
    def __init__(self, hueStart, hueEnd, satStart, satEnd, valStart, valEnd):
        self.hStart = hueStart
        self.hEnd = hueEnd
        self.sStart = satStart
        self.sEnd = satEnd
        self.vStart = valStart
        self.vEnd = valEnd
        
        self.colors = []
        self.count = 0
        
    def hasColor(self, c):
        for col in self.colors:
            if hue(c) == hue(col) and saturation(c) == saturation(col) and brightness(c) == brightness(col):
                return True
        return False
        
    def addColor(self, c):
        self.count += 1
        
        if self.hasColor(c):
            return
        
        self.colors.append(c)
        
    def getColor(self):
        if len(self.colors) == 0:
            return
        hTot = 0
        sTot = 0
        vTot = 0
        for col in self.colors:
            hTot += hue(col)
            sTot += saturation(col)
            vTot += brightness(col)
            
        hTot /= len(self.colors)
        sTot /= len(self.colors)
        vTot /= len(self.colors)
        return color(hTot, sTot, vTot)

        
        
def groupColors(colors):
    groups = []
    colorMode(HSB, 360, 100, 100)
    for h in range(0, 60):
        hueGroups = []
        for s in range(0, 20):
            satGroups = []
            for v in range(0, 20):
                newGroup = ColorGroup(h*(360/30), (h+1)*(360/30), s*10, s*10+10, v*10, v*10+10)
                satGroups.append(newGroup)
            hueGroups.append(satGroups)
        groups.append(hueGroups)
        
    for c in colors:
        h = hue(c)
        s = saturation(c)
        v = brightness(c)
        hGroup = int(h/60)
        sGroup = int(s/20)
        vGroup = int(v/20)
        if hGroup == 6:
            hGroup = 5
        if sGroup == 5:
            sGroup = 4
        if vGroup == 5:
            vGroup = 4
        
        groups[hGroup][sGroup][vGroup].addColor(c)
        
    groupCategories = []
    for hGroup in groups:
        for sGroup in hGroup:
            for vGroup in sGroup:
                numColors = vGroup.count
                if numColors > 10000:
                    groupCategories.append(vGroup)
    
    newCols = []
    for group in groupCategories:
        newCols.append(group.getColor())
        
    return newCols
