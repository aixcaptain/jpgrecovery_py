import os, sys, binascii
global sector #섹터 위치 저장

def recovery(imagefile) :
    global sector
    status = os.stat(imagefile)
    filesize = status.st_size 
    print(imagefile,"의 크기 : ",filesize/(1024*1024),"Mb") #조사할려는 이미지의 크기 출력

    f = open(imagefile,'rb') #이미지 파일 일기

    sector = 0 #0번 섹터부터 찾기 시작

    while sector < filesize : #파일 사이즈 만큼 찾기
        read_disk(f)
        if sector %(1024*1024*100) == 0 :
            print ("남은 용량 %d / %d " %(sector,filesize))

    
    f.close

def read_disk(f) :
    global sector
    sub_sector = read_file(f)
    sector_hex = binascii.hexlify(sub_sector) #읽은 섹터의 바이너리 값을 헥스 값으로 변환
    findfooter = False #이미지의 끝을 찾앗나 체크

    if sector_hex[:8] == 'ffd8ffe0' : #JPG의 헤더는 FFD8FFE0이다 찾았다면 쓰기 시작
        prinf("이미지 파일 발견")
        jpgfile = open("recovery/"+str(sector)+".jpg","wb")
        jpgfile.write(sub_sector)

        while findfooter == False : #이미지의 끝을 찾을때까지 쓰기
            sub_sector = read_file(f)
            sector_hex = binascii.hexlify(sub_sector)
            jpgfile.write(sub_sector)

            if sector_hex[:-4] == 'ffd9' : #jpg파일의 끝은 FFD9. 찾았다면 쓰기 완료
                findfooter = True 
        
        jpgfile.close()
        findfooter = False

def read_file(f) :
    global sector
    sub_sector = f.read(512) #이미지 파일을 512바이트만큼 읽음 참고로 1섹터의 사이즈는 512바이트
    f.tell() #현재 포인터 위치를 돌려줌
    sector = sector + 512 # 다음 섹터로 넘어감
    return sub_sector
    
if os.path.isdir('recovery') : #디렉토리 존재 여부 확인 
    pass

else :
    os.mkdir('recovery') # 'recovery' 디렉토리 생성

imagefile = sys.argv[1] #인자 값을 imagefile 변수에 저장

recovery(imagefile)