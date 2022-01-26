import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import json

# ---------- Variables
CALLBACKS = []
MOVEMENTS = []
ROTATION = []
THREAD_SWITCH = False
ROTATION_BUTTON = False
# ---------- End Variables


# ---------- Rubik's Cube User Interface
def CreateRubikUI():
    # Create the GUI
    WINDOW_NAME = "Rubik's Cube Controls"      
    myWindow = 'myWindowID'  
      
    if cmds.window(myWindow, exists=True):
        cmds.deleteUI(myWindow)
    if cmds.window(myWindow, exists=True):
        cmds.windowPref(myWindow, remove=True)
    cmds.window(myWindow, title=WINDOW_NAME, resizeToFitChildren=True)
    
    # ---- Main Layer
    mainColumn = cmds.columnLayout()
    form = cmds.formLayout(p=mainColumn)
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, p=form)

    # ---- Create Section
    createTab = cmds.columnLayout(adj = True, p=tabs)

    cmds.separator(h=5, style='none' )
    cmds.text("Properties of Rubik's Cube", fn = 'boldLabelFont', align = 'left', p = createTab)

    cmds.separator(h=10, style='doubleDash' )
    sizeSlider = cmds.intSliderGrp (l = "Size", min = 2, max = 8, field = True, v = 3, p = createTab)

    cmds.separator(h = 5, style='none')
    color_face_1 = cmds.colorSliderGrp (l = "Face 1 Color", rgb = (1, 1, 1), p = createTab)

    cmds.separator(h = 5, style='none')
    color_face_2 = cmds.colorSliderGrp (l = "Face 2 Color", rgb = (0, 0, 1), p = createTab)

    cmds.separator(h = 5, style='none')
    color_face_3 = cmds.colorSliderGrp (l = "Face 3 Color", rgb = (1, 0, 0), p = createTab)

    cmds.separator(h = 5, style='none')
    color_face_4 = cmds.colorSliderGrp (l = "Face 4 Color", rgb = (1, 1, 0), p = createTab)

    cmds.separator(h = 5, style='none')
    color_face_5 = cmds.colorSliderGrp (l = "Face 5 Color", rgb = (0, 1, 0), p = createTab)

    cmds.separator(h = 5, style='none')
    color_face_6 = cmds.colorSliderGrp (l = "Face 6 Color", rgb = (1, 0.3, 0), p = createTab)

    cmds.separator(h = 20, style='none')

    editTab = cmds.columnLayout(adj = True, p = tabs)
    fileTab = cmds.columnLayout(adj = True, p = tabs)

    cmds.button (l = "Create Rubik's Cube", command = lambda x: CreateRubikGeo(editTab, fileTab, cmds.intSliderGrp(sizeSlider, q=True, value=True), cmds.colorSliderGrp(color_face_1, q=True, rgb=True), 
        cmds.colorSliderGrp(color_face_2, q=True, rgb=True), cmds.colorSliderGrp(color_face_3, q=True, rgb=True), cmds.colorSliderGrp(color_face_4, q=True, rgb=True), 
        cmds.colorSliderGrp(color_face_5, q=True, rgb=True), cmds.colorSliderGrp(color_face_6, q=True, rgb=True)), p = createTab)
    # ---- End Creation Section   

    cmds.tabLayout( tabs, edit=True, tabLabel=((createTab, 'Create'), (editTab, 'Edit'), (fileTab,'File')))
    cmds.showWindow(myWindow)
# ---------- End Rubik's User Interface


# ---------- Rubik's Cube Geometry Creation
def CreateRubikGeo (editTab, fileTab, cubeSize, color_1, color_2, color_3, color_4, color_5, color_6):
    # -- Refresh UI
    RefreshUI (editTab, fileTab, cubeSize, color_1, color_2, color_3, color_4, color_5, color_6)


    # -- Scene Clean
    cmds.select (all=True)
    cmds.delete()

    if(cmds.objExists('RubikCube_grp')):
        cmds.delete('RubikCube_grp')

    if (len(CALLBACKS) != 0):
        for i in CALLBACKS:
            OpenMaya.MMessage.removeCallback(i)
            CALLBACKS.remove(i)
        del CALLBACKS[:]

    if (len(MOVEMENTS) != 0):        
        for i in MOVEMENTS:
            MOVEMENTS.remove(i)
        del MOVEMENTS[:]

    if (len(ROTATION) != 0):        
        for i in ROTATION:
            ROTATION.remove(i)
        del ROTATION[:]

    global ROTATION_BUTTON
    global THREAD_SWITCH
    ROTATION_BUTTON = False
    THREAD_SWITCH = False


    # -- Turn disabled
    THREAD_SWITCH = False

    # -- Cube Creation
    cube = cmds.polyCube (w = 1, h = 1, d = 1, n = "RubikCube_Piece_000", sx = 1, sy = 1, sz = 1, ax = (0,1,0), cuv = 4, ch = 1)
    cmds.polyBevel (cube, com = 0, fraction = 0.15, offsetAsFraction = 1, autoFit = 1, segments = 5, worldSpace = 1, 
        uvAssignment = 0, smoothingAngle = 30, fillNgons = 1, mergeVertices = 1, mergeVertexTolerance = 0.0001, miteringAngle = 100, angleTolerance = 180, ch = 1)  


    # -- Rubik's Cube Row
    cmds.select("RubikCube_Piece_000", replace = True)
    if (cubeSize % 2) == 0:
        offset = -(cubeSize / 2 - 0.5)
    else:
        offset = -(cubeSize / 2)

    cmds.move(offset, 0, 0, r = True)
    cmds.duplicate(rr = True)
    cmds.move(1, 0, 0, r = True)

    if (cubeSize > 2):
        for i in range(cubeSize - 2):
            cmds.duplicate(rr = True, st = True)


    # -- Rubik's Cube Face
    cmds.select (all = True)

    if (cubeSize % 2) == 0:
        offset = -(cubeSize / 2 - 0.5)
    else:
        offset = -(cubeSize / 2)

    cmds.move(0, offset, 0, r = True)
    cmds.duplicate(rr = True)
    cmds.move(0, 1, 0, r = True)

    if (cubeSize > 2):
        for i in range(cubeSize - 2):
            cmds.duplicate(rr = True, st = True)
            

    # -- Rubik's Cube Depth
    cmds.select (all = True)

    if (cubeSize % 2) == 0:
        offset = -(cubeSize / 2 - 0.5)
    else:
        offset = -(cubeSize / 2)
    
    cmds.move(0, 0, offset, r = True)
    cmds.duplicate(rr = True)
    cmds.move(0, 0, 1, r = True)

    if (cubeSize > 2):
        for i in range(cubeSize - 2):
            cmds.duplicate(rr = True, st = True)

    # -- Optimization
    cmds.select (allDagObjects = True)    
    RubikInternalCubesErasure (cubeSize, cmds.ls(selection = True))


    # -- Cubes origin relocation
    cmds.select (allDagObjects = True)
    for i in range (cubeSize*cubeSize*cubeSize):
        if (i < 10):
            geo = "RubikCube_Piece_00" + str(i)
        elif (i < 100):
            geo = "RubikCube_Piece_0" + str(i)
        else:
            geo = "RubikCube_Piece_" + str(i)

        if (cmds.objExists (geo)):
            scale = geo + '.scalePivot'
            rotation = geo + '.rotatePivot'
            cmds.move (0, 0, 0, scale, rotation)


    # -- Rename
    cmds.select (allDagObjects = True)
    for i in cmds.ls(selection = True):
        cmds.rename (i, i + '_geo')


    # -- Cubes are coloured
    cmds.select (allDagObjects = True)
    CreateRubikTextures (cubeSize, cmds.ls(selection = True), color_1, color_2, color_3, color_4, color_5, color_6)    


    # -- Group Geometry
    cmds.select (cmds.ls('*_geo'))
    cmds.group (n = "RubikCube_geo_grp")

    cmds.select ("RubikCube_geo_grp")
    cmds.group (n = "RubikCube_grp")


    # -- Create Skeletal Hierarchy
    CreateRubikSkeletalHierarchy (cubeSize, color_1, color_2, color_3, color_4, color_5, color_6)
# ---------- End Rubik's Cube Geometry Creation


# ---------- Refresh Edit Tab
def RefreshUI (editTab, fileTab, cubeSize, color_1_slider, color_2_slider, color_3_slider, color_4_slider, color_5_slider, color_6_slider):
    # -- Clear Layout
    elementsSelection = cmds.columnLayout(editTab, q = True, ca = True)
    if elementsSelection:
        if len(elementsSelection) > 0:
            for i in elementsSelection:
                cmds.deleteUI(i)


    elementsSelection = cmds.columnLayout(fileTab, q = True, ca = True)
    if elementsSelection:
        if len(elementsSelection) > 0:
            for i in elementsSelection:
                cmds.deleteUI(i)

    # ---- Edit Section
    cmds.separator(h=5, style='none', p = editTab)
    cmds.text("Movement of Rubik's Cube", fn = 'boldLabelFont', align = 'left', p = editTab)    
    cmds.separator (h = 5, style = 'none', p = editTab)

    controllersSelection = cmds.ls('*_controller')
    layoutId = []
    mainLayoutId = []
    index = 0
    for i in range (6):
        cmds.separator(h=10, style='doubleDash', p = editTab)
        mainLayoutId.append(cmds.rowColumnLayout (numberOfColumns = 3, columnWidth = ([1, 250], [2, 50], [3, 100]), p = editTab))
        cmds.text("Face " + str(i) +  " Movements     ", align = "right", p = mainLayoutId[i])
        if i == 0:
            cmds.text("    ", bgc = (color_1_slider[0], color_1_slider[1], color_1_slider[2]), align = 'left', p = mainLayoutId[i])
        elif i == 1:
            cmds.text("    ", bgc = (color_2_slider[0], color_2_slider[1], color_2_slider[2]), align = 'left', p = mainLayoutId[i])
        elif i == 2:
            cmds.text("    ", bgc = (color_3_slider[0], color_3_slider[1], color_3_slider[2]), align = 'left', p = mainLayoutId[i])
        elif i == 3:
            cmds.text("    ", bgc = (color_4_slider[0], color_4_slider[1], color_4_slider[2]), align = 'left', p = mainLayoutId[i])
        elif i == 4:
            cmds.text("    ", bgc = (color_5_slider[0], color_5_slider[1], color_5_slider[2]), align = 'left', p = mainLayoutId[i])
        elif i == 5:
            cmds.text("    ", bgc = (color_6_slider[0], color_6_slider[1], color_6_slider[2]), align = 'left', p = mainLayoutId[i])
        cmds.separator (h = 5, style = 'none', p = editTab)
        layoutId.append(cmds.rowColumnLayout (numberOfColumns = 2, columnWidth = [(1, 200), (2, 200)], cs = ((1, 1), (2, 5), (3, 5)), rs = ((1, 5), (2, 5)), p = editTab))
        if (cubeSize < 4):        
            face_number = i
            from functools import partial
            cmds.button(l = "Rotate Left", command = partial (ControllerRotationButton, cubeSize, face_number, 0, -1), p = layoutId [index])
            cmds.button(l = "Rotate Right", command = partial (ControllerRotationButton, cubeSize, face_number, 0, 1), p = layoutId [index])
        else:
            for j in range ( int ( int (cubeSize / 2))):
                face_number = i
                layer = j
                from functools import partial
                cmds.button(l = "Rotate Layer " + str(j) + " Left", command = partial (ControllerRotationButton, cubeSize, face_number, layer, -1), p = layoutId [index])
                cmds.button(l = "Rotate Layer " + str(j) + " Right", command = partial (ControllerRotationButton, cubeSize, face_number, layer, 1), p = layoutId [index])
        index += 1
    cmds.separator (h = 10, style = 'none', p = editTab)
    cmds.button (l = 'Solve Rubik Cube', command = lambda x: SolveRubiksCube(cubeSize), p = editTab)
    # ---- End Edit Section

    # ---- File Section
    cmds.separator (h = 10, style = 'none', p = fileTab)
    cmds.text("Features of Rubik's Cube", fn = 'boldLabelFont', align = 'left', p = fileTab)
    cmds.separator(h = 10, style = 'doubleDash', p = fileTab)

    cmds.text("Path where Json file will be save", align = "left", p = fileTab)
    cmds.separator (h = 5, style = 'none', p = fileTab)
    dirExplorer = cmds.rowColumnLayout (numberOfColumns = 2, columnWidth = [(1, 325), (2, 75)], cs = ((1, 1), (2, 5), (3, 5)), rs = ((1, 5), (2, 5)), p = fileTab)    
    
    dirPath = cmds.textField(tx = 'C:\Users\Public\Documents', w = 250, h = 25, p = dirExplorer)
    dirLoadBtn = cmds.button(w = 50, h = 25, label = "Path", command = lambda x: SelectDirectory (dirPath), p  = dirExplorer)
    cmds.separator (h = 10, style = 'none', p = fileTab)

    fileLayout = cmds.rowColumnLayout (numberOfColumns = 2, columnWidth = [(1, 200), (2, 200)], cs = ((1, 1), (2, 5), (3, 5)), rs = ((1, 5), (2, 5)), p = fileTab)    
    cmds.button (l = "Export JSON", command = lambda x: JsonExporter(cubeSize, cmds.textField (dirPath, q = True, text = True)), p = fileLayout)

    cmds.separator (h = 10, style = 'none', p = fileTab)
    cmds.separator (h = 10, style = 'none', p = fileTab)
    cmds.text("Path of the Json file that will be read", align = "left", p = fileTab)
    cmds.separator (h = 5, style = 'none', p = fileTab)
    cmds.text("**** Cube of the file must have the same size than the current cube ****", align = "center", p = fileTab)
    cmds.separator (h = 5, style = 'none', p = fileTab)
    fileExplorer = cmds.rowColumnLayout (numberOfColumns = 2, columnWidth = [(1, 325), (2, 75)], cs = ((1, 1), (2, 5), (3, 5)), rs = ((1, 5), (2, 5)), p = fileTab)    
    filePath = cmds.textField(tx = 'C:\Users\Public\Documents', w = 250, h = 25, p = fileExplorer)
    fileLoadBtn = cmds.button(w = 50, h = 25, label = "Path", command = lambda x: SelectFile (filePath), p  = fileExplorer)
    cmds.separator(h=5, style='none', p = fileTab)

    fileLayout = cmds.rowColumnLayout (numberOfColumns = 2, columnWidth = [(1, 200), (2, 200)], cs = ((1, 1), (2, 5), (3, 5)), rs = ((1, 5), (2, 5)), p = fileTab)    
    cmds.button (l = "Import JSON", command = lambda x: JsonImporter(cmds.textField (filePath, q = True, text = True), cubeSize), p = fileLayout)
    # ---- End File Section
# ---------- End Refresh Edit Tab


# ---------- Rubik's Cube Internal Cubes Erasure
def RubikInternalCubesErasure (cubeSize, selection):
    if (cubeSize % 2) == 0:
        offset = (cubeSize / 2 - 0.5) - 0.1
    else:
        offset = (cubeSize / 2) - 0.1

    counter = 0
    for i in selection:
        cubePosX = abs(cmds.getAttr (i + '.tx'))
        cubePosY = abs(cmds.getAttr (i + '.ty'))
        cubePosZ = abs(cmds.getAttr (i + '.tz'))

        if cubePosX < offset and cubePosY < offset and cubePosZ < offset:
            cmds.delete (i)
            counter += 1

    
    cmds.select (clear = True)
# ---------- End Rubik's Cube Internal Cubes Erasure


# ---------- Rubik's Cube Texture
def CreateRubikTextures (cubeSize, selection, color_1_slider, color_2_slider, color_3_slider, color_4_slider, color_5_slider, color_6_slider):
    # -- All cubes are coloured black
    black = cmds.shadingNode ("blinn", asShader = True)
    cmds.setAttr(black + '.color', 0, 0, 0)
    cmds.select(all = True)
    cmds.hyperShade(assign = black)

    color_1 = cmds.shadingNode ("blinn", asShader = True)
    cmds.setAttr (color_1 + '.color', color_1_slider[0], color_1_slider[1], color_1_slider[2])

    color_2 = cmds.shadingNode ("blinn", asShader = True)
    cmds.setAttr (color_2 + '.color', color_2_slider[0], color_2_slider[1], color_2_slider[2])

    color_3 = cmds.shadingNode ("blinn", asShader = True)
    cmds.setAttr (color_3 + '.color', color_3_slider[0], color_3_slider[1], color_3_slider[2])

    color_4 = cmds.shadingNode ("blinn", asShader = True)
    cmds.setAttr (color_4 + '.color', color_4_slider[0], color_4_slider[1], color_4_slider[2])

    color_5 = cmds.shadingNode ("blinn", asShader = True)
    cmds.setAttr (color_5 + '.color', color_5_slider[0], color_5_slider[1], color_5_slider[2])

    color_6 = cmds.shadingNode ("blinn", asShader = True)
    cmds.setAttr (color_6 + '.color', color_6_slider[0], color_6_slider[1], color_6_slider[2])

    if (cubeSize % 2) == 0:
        offset = (cubeSize / 2 - 0.5) - 0.1
    else:
        offset = (cubeSize / 2) - 0.1

    for i in selection:
        cubePosX = cmds.getAttr (i + '.tx')
        cubePosY = cmds.getAttr (i + '.ty')
        cubePosZ = cmds.getAttr (i + '.tz')

        if cubePosZ < - offset:
            material = i + '.f[5]'
            cmds.select (material)
            cmds.hyperShade(assign = color_1)
        if cubePosX < - offset: 
            material = i + '.f[2]'
            cmds.select (material)
            cmds.hyperShade(assign = color_2)
        if cubePosX > offset:
            material = i + '.f[3]'
            cmds.select (material)
            cmds.hyperShade(assign = color_3)
        if cubePosZ > offset:
            material = i + '.f[1]'
            cmds.select (material)
            cmds.hyperShade(assign = color_4)
        if cubePosY > offset:
            material = i + '.f[4]'
            cmds.select (material)
            cmds.hyperShade(assign = color_5)
        if cubePosY < - offset:
            material = i + '.f[0]'
            cmds.select (material)
            cmds.hyperShade(assign = color_6)

    cmds.select (clear = True)
# ---------- End Rubik's Cube Texture


# ---------- Rubik's Cube Skeleton Creation
def CreateRubikSkeletalHierarchy (cubeSize, color_1_slider, color_2_slider, color_3_slider, color_4_slider, color_5_slider, color_6_slider):
    # -- Cube's joints and bind
    cubesSelection = cmds.ls ('*_geo', o = True)
    for i in cubesSelection:        
        cubePosX = cmds.getAttr (i + '.translateX')
        cubePosY = cmds.getAttr (i + '.translateY')
        cubePosZ = cmds.getAttr (i + '.translateZ')
        name = i.split('_')
        cmds.select (i)
        newJoint = cmds.joint (n = name[0] + '_' + name[1] + '_' + name[2] + "_joint", p = (cubePosX, cubePosY, cubePosZ))
        cmds.skinCluster(i, newJoint)

    # -- Root joint
    cmds.joint(n = 'RubikCube_Root', p = (0, 0, 0,))

    # -- Re-organize hierarchy
    cmds.select (clear = True)
    jointsSelection = cmds.ls ('*_joint')
    cmds.select (jointsSelection)
    cmds.select ('RubikCube_Root', add = True)
    cmds.group (n = "RubikCube_joint_grp", p = 'RubikCube_grp')
    cmds.parent(jointsSelection, 'RubikCube_Root')
    cmds.select(clear = True)

    # -- Create Controllers
    CreateRubikControllers (cubeSize, color_1_slider, color_2_slider, color_3_slider, color_4_slider, color_5_slider, color_6_slider)
# ---------- End Rubik's Cube Skeleton Creation


# ---------- Rubik's Cube Controllers
def CreateRubikControllers (cubeSize, color_1_slider, color_2_slider, color_3_slider, color_4_slider, color_5_slider, color_6_slider):
    # -- Number of controllers per side
    numberControllers = int (cubeSize / 2)

    if (cubeSize % 2) == 0:
        position = (cubeSize / 2 - 0.5)
    else:
        position = (cubeSize / 2)

    for i in range(6):
        offset = numberControllers + 2
        for j in range(numberControllers):
            if (numberControllers == 1):
                circleName = "RubikCube_Face_" + str(i) + '_controller'
            else:
                circleName = "RubikCube_Face_" + str(i) + '_' + str(j) + '_controller'

            if i == 0:
                cmds.circle (nr = (0, 0, 1), n = circleName)
                cmds.select(circleName)
                cmds.move(0, 0, -offset - position, r = True)
                cmds.setAttr (circleName + '.rx', lock = True)
                cmds.setAttr (circleName + '.ry', lock = True)
                cmds.setAttr (circleName + '.overrideEnabled', 1)
                cmds.setAttr (circleName + '.overrideRGBColors', 1)
                cmds.setAttr (circleName + '.overrideColorRGB', color_1_slider[0], color_1_slider[1], color_1_slider[2])
                offset -= 1

            elif i == 1:
                cmds.circle (nr = (1, 0, 0), n = circleName)
                cmds.select(circleName)
                cmds.move(-offset - position, 0, 0, r = True)
                cmds.setAttr (circleName + '.ry', lock = True)
                cmds.setAttr (circleName + '.rz', lock = True)
                cmds.setAttr (circleName + '.overrideEnabled', 1)
                cmds.setAttr (circleName + '.overrideRGBColors', 1)
                cmds.setAttr (circleName + '.overrideColorRGB', color_2_slider[0], color_2_slider[1], color_2_slider[2])
                offset -= 1

            elif i == 2:
                cmds.circle (nr = (-1, 0, 0), n = circleName)
                cmds.select(circleName)
                cmds.move(offset + position, 0, 0, r = True)
                cmds.setAttr (circleName + '.ry', lock = True)
                cmds.setAttr (circleName + '.rz', lock = True)
                cmds.setAttr (circleName + '.overrideEnabled', 1)
                cmds.setAttr (circleName + '.overrideRGBColors', 1)
                cmds.setAttr (circleName + '.overrideColorRGB', color_3_slider[0], color_3_slider[1], color_3_slider[2])
                offset -= 1

            elif i == 3:
                cmds.circle (nr = (0, 0, -1), n = circleName)
                cmds.select(circleName)
                cmds.move(0, 0, offset + position, r = True)
                cmds.setAttr (circleName + '.rx', lock = True)
                cmds.setAttr (circleName + '.ry', lock = True)
                cmds.setAttr (circleName + '.overrideEnabled', 1)
                cmds.setAttr (circleName + '.overrideRGBColors', 1)
                cmds.setAttr (circleName + '.overrideColorRGB', color_4_slider[0], color_4_slider[1], color_4_slider[2])
                offset -= 1

            elif i == 4:
                cmds.circle (nr = (0, 1, 0), n = circleName)
                cmds.select(circleName)
                cmds.move(0, offset + position, 0, r = True)
                cmds.setAttr (circleName + '.rx', lock = True)
                cmds.setAttr (circleName + '.rz', lock = True)
                cmds.setAttr (circleName + '.overrideEnabled', 1)
                cmds.setAttr (circleName + '.overrideRGBColors', 1)
                cmds.setAttr (circleName + '.overrideColorRGB', color_5_slider[0], color_5_slider[1], color_5_slider[2])
                offset -= 1

            elif i == 5:
                cmds.circle (nr = (0, -1, 0), n =  circleName)
                cmds.select(circleName)
                cmds.move(0, -offset - position, 0, r = True)
                cmds.setAttr (circleName + '.rx', lock = True)
                cmds.setAttr (circleName + '.rz', lock = True)
                cmds.setAttr (circleName + '.overrideEnabled', 1)
                cmds.setAttr (circleName + '.overrideRGBColors', 1)
                cmds.setAttr (circleName + '.overrideColorRGB', color_6_slider[0], color_6_slider[1], color_6_slider[2])
                offset -= 1                

            cmds.setAttr (circleName + '.tx', lock = True)
            cmds.setAttr (circleName + '.ty', lock = True)
            cmds.setAttr (circleName + '.tz', lock = True)
            cmds.setAttr (circleName + '.sx', lock = True)
            cmds.setAttr (circleName + '.sy', lock = True)
            cmds.setAttr (circleName + '.sz', lock = True)

        cmds.select (clear = True)
        cmds.parent(cmds.ls ('*_controller'), 'RubikCube_Root')

    cmds.select (clear = True)  

    # -- Thread enabled
    global THREAD_SWITCH
    THREAD_SWITCH = True
    
    # -- Thread created
    global CALLBACKS
    global thread        
    thread = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", ControllersBehaviour)
    CALLBACKS.append(thread)
# ---------- End Rubik's Cube Controllers


# ---------- Cubes Selection by Controller
def SelectionByController(controller):
    # -- Checks if some controller has joints attached
    prevController = ''

    controllersSelection = cmds.ls ('*_controller')
    for i in controllersSelection:
        childs = cmds.listRelatives(i, c = True, type = 'joint')
        if childs:
            prevController = i
            break

    # -- if some controller has joints attached, his rotation must be rounded 
    if prevController != '':
        RoundControllerRotation(prevController, controller, True)

    controllerName = controller.split('_')
    if (len (controllerName) < 5):
        JointsSelectionByFace(int(controllerName[2]), 0)
        cmds.parent(cmds.ls(selection = True), controller)
        
    else:
        JointsSelectionByFace(int(controllerName[2]), int(controllerName[3]))
        cmds.parent(cmds.ls(selection = True), controller)

    cmds.select(clear = True)    
# ---------- End Cubes Selection by Controller


# ---------- Rubik's Cube Joints Selection by Face
def JointsSelectionByFace (face_number, layer):
    numberCubes = cmds.ls('*_geo')
    cubeSize = 0

    # numCubes = 6 *size * size - 12 * size + 8
    if len(numberCubes) == 8:
        cubeSize = 2
    elif len(numberCubes) == 26:
        cubeSize = 3
    elif len(numberCubes) == 56:
        cubeSize = 4
    elif len(numberCubes) == 98:
        cubeSize = 5
    elif len(numberCubes) == 152:
        cubeSize = 6
    elif len(numberCubes) == 216:
        cubeSize = 7
    elif len(numberCubes) == 296:
        cubeSize = 8

    if (cubeSize % 2) == 0:
        offset = (cubeSize / 2 - 0.5)
    else:
        offset = (cubeSize / 2)

    cmds.select(cmds.ls('*_joint'))
    jointsSelection = cmds.ls('*_joint')

    for i in jointsSelection:
        p = cmds.xform(i, q=True, t=True, ws=True)       
        cubePosX = round(p[0], 2)
        cubePosY = round(p[1], 2)
        cubePosZ = round(p[2], 2)
        if(cubePosX > offset or cubePosX< -offset):
            cubePosX = 0
        if(cubePosY > offset or cubePosY < -offset):
            cubePosY = 0
        if(cubePosZ > offset or cubePosZ < -offset):
            cubePosZ = 0

        if (face_number == 0):
            if (cubePosZ != -offset + layer):
                cmds.select (i, deselect = True)
        elif (face_number == 1):
            if (cubePosX != -offset + layer):
                cmds.select (i, deselect = True)
        elif (face_number == 2):
            if (cubePosX != offset - layer):
                cmds.select (i, deselect = True)
        elif (face_number == 3):
            if (cubePosZ != offset - layer):
                cmds.select (i, deselect = True)
        elif (face_number == 4):
            if (cubePosY != offset - layer):            
                cmds.select (i, deselect = True)
        elif (face_number == 5):
            if (cubePosY != -offset + layer):
                cmds.select (i, deselect = True)
# ---------- End Rubik's Cube Joints Selection by Face


# ---------- Round Controller Rotation
def RoundControllerRotation (controller, nextController, registerMovement):
    controllerRotX = cmds.getAttr (controller + '.rx')
    controllerRotY = cmds.getAttr (controller + '.ry')
    controllerRotZ = cmds.getAttr (controller + '.rz')    
    rotationInexact = False

    if (controllerRotX != ROTATION [0]) or (controllerRotY != ROTATION [1]) or (controllerRotZ != ROTATION [2]) and ROTATION_BUTTON == False:
        
        controllerSegments = controller.split('_')
        face_number = int(controllerSegments[2])
        cmds.select(controller)

        if face_number == 0 or face_number == 3:
            side = controllerRotZ / abs(controllerRotZ)        
            approx = int (controllerRotZ / 45)
            rotation = int(abs(controllerRotZ / 90))  
        elif face_number == 1 or face_number == 2:            
            side = controllerRotX / abs(controllerRotX)        
            approx = int (controllerRotX / 45)
            rotation = int(abs(controllerRotX / 90))
        elif face_number == 4 or face_number == 5:
            side = controllerRotY / abs(controllerRotY)        
            approx = int (controllerRotY / 45)
            rotation = int(abs(controllerRotY / 90))  

        if (rotation > 3):
            rotation = rotation % 4

        if (approx % 2 != 0 and rotation == 0):
            rotation += 1
        elif (approx % 2 != 0):
            rotation +=1
        
        if side == -1:
            rotationValue = 360 - (rotation * 90)
        else:
            rotationValue = rotation * 90
       
        if face_number == 0 or face_number == 3:
            cmds.rotate (0, 0, str(rotationValue) + 'deg')
            currentRotation = int (rotationValue - ROTATION[2])     
        elif face_number == 1 or face_number == 2:
            cmds.rotate (str(rotationValue) + 'deg', 0, 0)
            currentRotation = int (rotationValue - ROTATION[0])
        elif face_number == 4 or face_number == 5:
            cmds.rotate (0, str(rotationValue) + 'deg', 0)
            currentRotation = int (rotationValue - ROTATION[1])
    
        if currentRotation > 360:
            currentRotation -= 360
        elif currentRotation < -360:
            currentRotation += 360
        if currentRotation == 360:
            currentRotation = 0

        if abs(currentRotation) == 90:
            RegisterMovement (controller, int(currentRotation))
        elif abs(currentRotation) == 180:
            RegisterMovement (controller, int(currentRotation / 2))
            RegisterMovement (controller, int(currentRotation / 2))
        elif abs(currentRotation) == 270:
            RegisterMovement (controller, int(currentRotation / 3))
            RegisterMovement (controller, int(currentRotation / 3))
            RegisterMovement (controller, int(currentRotation / 3))

    if (registerMovement == True):
        if (len(ROTATION) != 0):        
            for i in ROTATION:
                ROTATION.remove(i)
            del ROTATION[:]

        ROTATION.append(cmds.getAttr (nextController + '.rx'))
        ROTATION.append(cmds.getAttr (nextController + '.ry'))
        ROTATION.append(cmds.getAttr (nextController + '.rz'))

        cmds.parent(cmds.ls('*_joint'), 'RubikCube_Root')
# ---------- End Round Controller Rotation


# ---------- Rotation Fit
def RotationFit ():
    if len (ROTATION) == 0:
        controllersSelection = cmds.ls('*_controller')
        controllerRotX = cmds.getAttr (controllersSelection[0] + '.rx')
        controllerRotY = cmds.getAttr (controllersSelection[0] + '.ry')
        controllerRotZ = cmds.getAttr (controllersSelection[0] + '.rz')
        ROTATION.append(controllerRotX)
        ROTATION.append(controllerRotY)
        ROTATION.append(controllerRotZ)
        cmds.select(clear = True)

    # -- Checks if some controller has joints attached
    prevController = ''

    controllersSelection = cmds.ls ('*_controller')
    for i in controllersSelection:
        childs = cmds.listRelatives(i, c = True, type = 'joint')
        if childs:
            prevController = i
            break

    # -- if some controller has joints attached, his rotation must be rounded 
    if prevController != '':
        RoundControllerRotation(prevController, prevController, False)
    cmds.select (clear = True)
# ---------- End Rotation Fit


# ---------- Rotate Controller by Button
def ControllerRotationButton (cubeSize, face_number, layer, clockwise, _none):
    # -- Thread disabled
    global THREAD_SWITCH
    THREAD_SWITCH = False

    RotationFit()

    if cubeSize < 4:
        controller = 'RubikCube_Face_' + str(face_number) + '_controller'
        cmds.select (controller)
    else:
        controller = 'RubikCube_Face_' + str(face_number) + '_' + str(layer) + '_controller'
        cmds.select (controller)

    prevController = ''
    controllersSelection = cmds.ls ('*_controller')
    for i in controllersSelection:
        childs = cmds.listRelatives(i, c = True, type = 'joint')
        if childs:
            prevController = i
            break

    # -- if some controller has joints attached, must be reset
    if prevController != '':
        cmds.parent (cmds.ls('*_joint'), 'RubikCube_Root')

    JointsSelectionByFace(face_number, layer)
    cmds.parent (cmds.ls(selection = True), controller)
    cmds.select (controller)

    if face_number == 0 or face_number == 3:
        rotation = 90 * clockwise / 5
        timeStart = cmds.timerX()
        stepIndex = 0
        while(1):
            totalTime = cmds.timerX (startTime = timeStart)
            if (totalTime > 0.06):
                cmds.rotate (0, 0, str(rotation) + 'deg',cmds.ls (selection = True), r = True)
                stepIndex += 1
                cmds.refresh ()
                timeStart = cmds.timerX()
            if stepIndex >= 5:
                break
        RegisterMovement (controller, rotation*5)         

    elif face_number == 1 or face_number == 2:
        rotation = 90 * clockwise / 5
        timeStart = cmds.timerX()
        stepIndex = 0
        while(1):
            totalTime = cmds.timerX (startTime = timeStart)
            if (totalTime > 0.06):
                cmds.rotate (str(rotation) + 'deg', 0, 0,cmds.ls (selection = True), r = True)
                stepIndex += 1
                cmds.refresh ()
                timeStart = cmds.timerX()
            if stepIndex >= 5:
                break
        RegisterMovement (controller, rotation*5)

    elif face_number == 4 or face_number == 5:
        rotation = 90 * clockwise / 5
        timeStart = cmds.timerX()
        stepIndex = 0
        while(1):
            totalTime = cmds.timerX (startTime = timeStart)
            if (totalTime > 0.06):
                cmds.rotate (0, str(rotation) + 'deg', 0,cmds.ls (selection = True), r = True)
                stepIndex += 1
                cmds.refresh ()
                timeStart = cmds.timerX()
            if stepIndex >= 5:
                break 
        RegisterMovement (controller, rotation*5)

    if (len(ROTATION) != 0):        
        for i in ROTATION:
            ROTATION.remove(i)
        del ROTATION[:]

    ROTATION.append(cmds.getAttr (controller + '.rx'))
    ROTATION.append(cmds.getAttr (controller + '.ry'))
    ROTATION.append(cmds.getAttr (controller + '.rz'))

    # -- Thread enabled
    THREAD_SWITCH = True
    cmds.select (clear = True)
# ---------- Rotate Controller by Button    


# ---------- Seleect Directory
def SelectDirectory (path):
    folder = cmds.fileDialog2(cap = "Select Folder", fm = 3)
    cmds.textField(path, edit = True, text = folder[0])
# ---------- End Select Directory


# ---------- JSON Exporter
def JsonExporter (cubeSize, path):
    outData = {
                "size":cubeSize, 
                "moves":{}
              }

    for i in range(len (MOVEMENTS)):
        outData["moves"][str(100000 + i)] = MOVEMENTS[i]

    date = cmds.date (d = True)
    time = cmds.date (t = True)
    dateSelection = date.split('/')
    timeSelection = time.split(':')

    sufix = str('_' + dateSelection[0]) + '_' + str(dateSelection[1]) + '_' + str(dateSelection[2]) + '_' + str(timeSelection[0]) + '-' + str(timeSelection[1]) + '-' + str(timeSelection[2])

    with open (path + '/rubikCube_with_size_' + str(cubeSize) + sufix + '.json' , 'w') as outfile:
        json.dump (outData, outfile, indent = 2, sort_keys=True)

    Pop_Up_Open ('Json Export', 'Json exported without errors')
# ---------- End JSON Exporter


# ---------- Select File
def SelectFile (path):
    file = cmds.fileDialog2(fileFilter = '*.json', cap = "Select Json", fm = 1)
    cmds.textField(path, edit = True, text = file[0])
# ---------- End Select File


# ---------- JSON Importer
def JsonImporter (path, cubeSize):
    try:
        from collections import OrderedDict
        with open (path) as infile:
            inData = json.load(infile, object_pairs_hook=OrderedDict)
    except IOError as e:
        print e
        Pop_Up_Open ('Json Import', 'Import Failed: Unable to open .json. Please, select a valid')

    if (inData["size"] == cubeSize):
        if (len(MOVEMENTS) == 0):
            # Thread disabled
            global THREAD_SWITCH
            THREAD_SWITCH = False

            for i in inData["moves"]:
                movement = inData["moves"][i]
                movementsSegments = movement.split('_')
                if cubeSize < 4:
                    controller = movementsSegments [0] + '_' + movementsSegments[1] + '_' + movementsSegments[2] + '_' + movementsSegments[3]
                    controllerSegments = controller.split('_')
                    rotation = int (movementsSegments [4])
                    face_number = int (controllerSegments [2])
                    layer = 0
                else:
                    controller = movementsSegments [0] + '_' + movementsSegments[1] + '_' + movementsSegments[2] + '_' + movementsSegments[3] + '_' + movementsSegments[4]
                    controllerSegments = controller.split('_')
                    rotation = int (movementsSegments [5])
                    face_number = int (controllerSegments [2])
                    layer = int (controllerSegments [3])

                prevController = ''
                controllersSelection = cmds.ls ('*_controller')
                for i in controllersSelection:
                    childs = cmds.listRelatives(i, c = True, type = 'joint')
                    if childs:
                        prevController = i
                        break

                # -- if some controller has joints attached, must be reset
                if prevController != '':
                    cmds.parent (cmds.ls('*_joint'), 'RubikCube_Root')

                JointsSelectionByFace(face_number, layer)
                cmds.parent (cmds.ls(selection = True), controller)
                cmds.select (controller)

                if face_number == 0 or face_number == 3:
                    cmds.rotate (0, 0, str (rotation) + 'deg', controller, r = True)           
                elif face_number == 1 or face_number == 2:
                    cmds.rotate (str (rotation) + 'deg', 0, 0, controller, r = True)       
                elif face_number == 4 or face_number == 5:
                    cmds.rotate (0, str (rotation) + 'deg', 0, controller, r = True)

                RegisterMovement (controller, rotation)

            prevController = ''
            controllersSelection = cmds.ls ('*_controller')
            for i in controllersSelection:
                childs = cmds.listRelatives(i, c = True, type = 'joint')
                if childs:
                    prevController = i
                    break

            # -- if some controller has joints attached, must be reset
            if prevController != '':
                cmds.parent (cmds.ls('*_joint'), 'RubikCube_Root')

            cmds.select(clear = True)

            # Thread enabled
            THREAD_SWITCH = True

            Pop_Up_Open ('Json Import', 'Json Imported without errors')   
        else:
            Pop_Up_Open ('Json Import', 'Import Failed: Cube has been moved before trying to import json.\n Please create a new cube')
    else:
        Pop_Up_Open ('Json Import', 'Import Failed: Cube stored in json file with different size')
# ---------- End JSON Importer


# ---------- Solve Rubik's Cube
def SolveRubiksCube (cubeSize):
    if len(MOVEMENTS) == 0:
        Pop_Up_Open ('Rubik Solver', 'Error Solving Cube: Rubik cube is alredy solved')
    else:
        # -- Thread disabled
        global THREAD_SWITCH
        THREAD_SWITCH = False

        RotationFit()

        print(len (MOVEMENTS))
        for i in range (len (MOVEMENTS) - 1, -1, -1):
            
            movementsSegments = MOVEMENTS[i].split('_')
            if cubeSize < 4:
                controller = movementsSegments [0] + '_' + movementsSegments[1] + '_' + movementsSegments[2] + '_' + movementsSegments[3]
                controllerSegments = controller.split('_')
                rotation = int (movementsSegments [4])
                face_number = int (controllerSegments [2])
                layer = 0
            else:
                controller = movementsSegments [0] + '_' + movementsSegments[1] + '_' + movementsSegments[2] + '_' + movementsSegments[3] + '_' + movementsSegments[4]
                controllerSegments = controller.split('_')
                rotation = int (movementsSegments [5])
                face_number = int (controllerSegments [2])
                layer = int (controllerSegments [3])
            
            cmds.parent (cmds.ls('*_joint'), 'RubikCube_Root')
            JointsSelectionByFace(face_number, layer)
            cmds.parent (cmds.ls(selection = True), controller)
            cmds.select(controller)

            maxSteps = 5
            if abs(rotation) == 90:
                maxSteps = 5
            elif abs(rotation) == 180:
                maxSteps = 10
            elif abs(rotation) == 270:
                maxSteps = 15

            rotation = -1 * rotation / maxSteps
            timeStart = cmds.timerX()
            stepIndex = 0

            
            if face_number == 0 or face_number == 3:               
                while(1):
                    totalTime = cmds.timerX (startTime = timeStart)
                    if (totalTime > 0.06):
                        cmds.rotate (0, 0, str(rotation) + 'deg', cmds.ls (selection = True), r = True)
                        stepIndex += 1
                        cmds.refresh ()
                        timeStart = cmds.timerX()
                    if stepIndex >= maxSteps:
                        break         

            elif face_number == 1 or face_number == 2:
                while(1):                        
                    totalTime = cmds.timerX (startTime = timeStart)
                    if (totalTime > 0.06):
                        cmds.rotate (str(rotation) + 'deg', 0, 0, cmds.ls (selection = True), r = True)
                        stepIndex += 1
                        cmds.refresh ()
                        timeStart = cmds.timerX()
                    if stepIndex >= maxSteps:
                        break

            elif face_number == 4 or face_number == 5: 
                while(1):                        
                    totalTime = cmds.timerX (startTime = timeStart)
                    if (totalTime > 0.06):
                        cmds.rotate (0, str(rotation) + 'deg', 0, cmds.ls (selection = True), r = True)
                        stepIndex += 1
                        cmds.refresh ()
                        timeStart = cmds.timerX()
                    if stepIndex >= maxSteps:
                        break

        if (len(MOVEMENTS) != 0):        
            for i in MOVEMENTS:
                MOVEMENTS.remove(i)
            del MOVEMENTS[:]

        prevController = ''
        controllersSelection = cmds.ls ('*_controller')
        for i in controllersSelection:
            childs = cmds.listRelatives(i, c = True, type = 'joint')
            if childs:
                prevController = i
                break

        # -- if some controller has joints attached, must be reset
        if prevController != '':
            cmds.parent (cmds.ls('*_joint'), 'RubikCube_Root')

        cmds.select(clear = True)

        # Thread enabled   
        THREAD_SWITCH = True    
# ---------- End Solve Rubik's Cube


# ---------- Register Movement
def RegisterMovement (controller, rotation):
    movementValue = controller + '_' + str(rotation)
    MOVEMENTS.append (movementValue)
    print ('Movement Stored: ' + movementValue)
# ---------- End Register Movement     


# ---------- Open Pop Up
def Pop_Up_Open (title, message):
    WINDOW_NAME = title
    myWindow = 'Pop Up' 

    if cmds.window(myWindow, exists=True):
        cmds.deleteUI(myWindow)

    window = cmds.window(myWindow, title=WINDOW_NAME, resizeToFitChildren=True)

    messageLayout = cmds.rowColumnLayout ()
    cmds.separator (h = 10, style = 'none', p = messageLayout)
    cmds.text('          ' + message + '          ', fn = 'boldLabelFont', align = 'left', p = messageLayout)
    cmds.separator(h = 15, style = 'none', p = messageLayout)
    cmds.button (l = "Close", command = lambda x: Pop_Up_Close(window), p = messageLayout)

    cmds.showWindow(window)
# ---------- End Pop Up


# ---------- Close Pop Up
def Pop_Up_Close (window):
    if cmds.window(window, exists=True):
        cmds.deleteUI(window)
# ---------- End Close Pop Up


# ---------- Thread Controllers Once they're selected
def ControllersBehaviour(*args, **kwargs):       
    if THREAD_SWITCH:
        mayaSelectedObjects = cmds.ls (selection = True)
        controllersSelection = cmds.ls ('*_controller')

        if (len(mayaSelectedObjects) == 1 and len(controllersSelection) > 0):
            for i in controllersSelection:
                if(mayaSelectedObjects[0] ==  i):
                    if len (ROTATION) == 0:
                        controllerRotX = cmds.getAttr (i + '.rx')
                        controllerRotY = cmds.getAttr (i + '.ry')
                        controllerRotZ = cmds.getAttr (i + '.rz')
                        ROTATION.append(controllerRotX)
                        ROTATION.append(controllerRotY)
                        ROTATION.append(controllerRotZ)

                    SelectionByController(i)
                    break

        cmds.select(clear = True)
        cmds.select(mayaSelectedObjects)
# ---------- End Thread Controllers Once they're selected


# ---------- Main Execution 
#if thread:
#    OpenMaya.MMessage.removeCallback(thread)
CreateRubikUI()