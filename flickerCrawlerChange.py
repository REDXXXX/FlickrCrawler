import flickrapi
import codecs
import os
import time

def download():
    api_key = ''
    secret = ''
    flickr = flickrapi.FlickrAPI(api_key, secret, format='parsed-json')
    # id='95794505@N06'
    photoId = codecs.open('photoId.txt', 'a', 'utf-8')
    userInfo = codecs.open('userInfo.txt', 'r', 'utf-8')
    temp = userInfo.readlines()
    userInfo.close()
    userInfo = codecs.open('userInfo.txt', 'a', 'utf-8')
    # 第一步，获取这个用户的照片，以及照片的喜欢者，将喜欢者加入待选集。
    beginTime=time.time()
    idList = []
    for l in temp:
        originId = l.split(';')[0]
        idList.append(originId)
    for id in idList:
        endTime=time.time()
        passedTime=endTime-beginTime;
        if passedTime%60==10:
            #每过十分钟就去重一次
            checkPhotoIdRepeat()
            checkUserIdRepeat()
        photosets = flickr.photosets_getList(user_id=id)
        # print(photosets)
        photoSets = []
        locationInfo = codecs.open('locationInfo.txt', 'a', 'utf-8');
        for l in photosets['photosets']['photoset']:
            photosetName = l['id']
            photoSets.append(photosetName)
        print(photoSets)
        for l in photoSets:
            out_photo = flickr.photosets_getPhotos(photoset_id=l, user_id=id)
            list = out_photo['photoset']['photo']
            for i in list:
                ids = i['id']
                owners = id
                photoId.write(str(ids) + ';' + owners + '\n')
                # 对于每一个照片，做以下三个事情，1.获取其详细信息，2.获取其地理位置，3.获取其喜爱者
                try:
                    photoGeo = flickr.photos_geo_getLocation(photo_id=ids)
                    photoGeo = photoGeo['photo']
                    photoid = photoGeo['id']
                    location = photoGeo['location']
                    latitude = location['latitude']
                    longitude = location['longitude']
                    country = location['country']['_content']
                    county = location['county']['_content']
                    region = location['region']['_content']
                    woeid = location['region']['woeid']
                    out_info = flickr.photos_getInfo(photo_id=ids)
                    date = out_info['photo']['dates']['taken']
                    locationInfo.write(
                        id + ';' + photoid + ';' + latitude + ',' + longitude + ';' + country + ';' + county + ';' + region + ';' + woeid + ';' + date + '\n')
                except Exception as e:
                    print(repr(e))
                try:
                    userList = flickr.photos_getFavorites(photo_id=ids)
                    userList = userList['photo']['person']
                    for i in userList:
                        nsid = i['nsid']
                        username = i['username']
                        realname = i['realname']
                        userInfo.write(nsid + ';' + username + ';' + realname + '\n')
                except Exception as e:
                    print(repr(e))
                    #第四步，对于一个user，获取其喜欢的照片，放入photoId里。为什么？因为既然他喜欢，说明这个照片比较特别，可能是因为这个照片本身质量较高
                    # 也有可能是因为这个照片对他来说有特别的意义。比如家人的照片等。因此，获取其喜欢的照片，还是很重要的。
                    '''
                        photoList = flickr.favorites_getList(user_id=nsid, per_page=500)
                        photos = photoList['photos']['photo']
            
                        for lss in photos:
                            id=lss['id']
                            owner=lss['owner']
                            photoId.write(id+';'+owner+'\n')
                        pages=photoList['photos']['pages']
                        count=2
                        while count<=pages:
                            photoList=flickr.favorites_getList(user_id=nsid,page=count,per_page=500)
                            photos = photoList['photos']['photo']
                            for lss in photos:
                                idAgain = lss['id']
                                owner = lss['owner']
                                photoId.write(idAgain + ';' + owner + '\n')

                            count=count+1
                        '''
                        # print(photoList)
                        # print(photoGeo)
                        # print(out_info)
                        # print(userList)


def checkUserIdRepeat():
    file1=codecs.open('userInfo.txt','r','utf-8')
    ids=file1.readlines()
    file1.close()
    print('去重前共有%d条数据'%(len(ids)))
    tempset=set()
    tempFile=codecs.open('temp.txt','w','utf-8')
    for l in ids:
        if l not in tempset:
            tempset.add(l)
            tempFile.write(l)
    tempFile.close()
    os.remove('userInfo.txt')
    os.rename('temp.txt','userInfo.txt')

def checkPhotoIdRepeat():
    file1=codecs.open('photoId.txt','r','utf-8')
    ids=file1.readlines()
    file1.close()
    print('去重前共有%d条数据'%(len(ids)))
    tempset=set()
    tempFile=codecs.open('temp.txt','w','utf-8')
    for l in ids:
        if l not in tempset:
            tempset.add(l)
            tempFile.write(l)
    tempFile.close()
    os.remove('photoId.txt')
    os.rename('temp.txt','photoId.txt')

if __name__=='__main__':
    download()


