//=============================================================================================================================
//
// Copyright (c) 2015-2022 VisionStar Information Technology (Shanghai) Co., Ltd. All Rights Reserved.
// EasyAR is the registered trademark or trademark of VisionStar Information Technology (Shanghai) Co., Ltd in China
// and other countries for the augmented reality technology developed by VisionStar Information Technology (Shanghai) Co., Ltd.
//
//=============================================================================================================================

using easyar;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;
using Dummiesman;
using System.Text;

namespace ImageTracking_TargetOnTheFly
{
    public class TargetOnTheFlySample : MonoBehaviour
    {
        public ImageTrackerFrameFilter Filter;
        public GameObject Cube;
        public Button BackButton;
        public Material mat;
        public Material white;
        public Material plane;

        private bool creating;
        private string directory;
        private Dictionary<string, ImageTargetController> imageTargetDic = new Dictionary<string, ImageTargetController>();

        private void Start()
        {
            directory = Path.Combine(Application.persistentDataPath, "TargetOnTheFly");
            if (!Directory.Exists(directory))
                Directory.CreateDirectory(directory);
            LoadLocalTargets();

            var launcher = "AllSamplesLauncher";
            if (Application.CanStreamedLevelBeLoaded(launcher))
            {
                var button = BackButton.GetComponent<Button>();
                button.onClick.AddListener(() => { UnityEngine.SceneManagement.SceneManager.LoadScene(launcher); });
            }
            else
            {
                BackButton.gameObject.SetActive(false);
            }
        }

        private void LoadLocalTargets()
        {
            Dictionary<string, string> imagefilesDic = GetImagesWithDir(directory);
            foreach (var obj in imagefilesDic.Where(obj => !imageTargetDic.ContainsKey(obj.Key)))
            {
                CreateImageTarget(obj.Key, obj.Value);
            }
        }

        private Dictionary<string, string> GetImagesWithDir(string path)
        {
            Dictionary<string, string> imagefilesDic = new Dictionary<string, string>();
            foreach (var file in Directory.GetFiles(path))
            {
                if (Path.GetExtension(file) == ".jpg" || Path.GetExtension(file) == ".bmp" || Path.GetExtension(file) == ".jpg")
                    imagefilesDic.Add(Path.GetFileName(file), file);
            }
            return imagefilesDic;
        }

        private IEnumerator TakePhotoCreateTarget()
        {
            creating = true;

            yield return new WaitForEndOfFrame();

            if (!creating)
            {
                yield break;
            }

            Texture2D photo = new Texture2D(Screen.width, (Screen.height *3 )/ 4, TextureFormat.RGB24, false);
            photo.ReadPixels(new Rect(0, Screen.height / 5, Screen.width , Screen.height), 0, 0, false);
            photo.Apply();

            byte[] data = photo.EncodeToJPG();
            Destroy(photo);

            string photoName = "photo" + DateTime.Now.Ticks + ".jpg";
            string photoPath = Path.Combine(directory, photoName);
            File.WriteAllBytes(photoPath, data);
            CreateImageTarget(photoName, photoPath);

            
            // Create a Web Form
            WWWForm form = new WWWForm();
            form.AddField("frameCount", Time.frameCount.ToString());
            form.AddBinaryData("file", data, "screenShot.jpg", "image/jpg");
            string URL = "http://192.168.4.171:5000/";

            // Upload to a cgi script
            WWW w = new WWW(URL, form);
            yield return w;
            if (!string.IsNullOrEmpty(w.error)) {
                    print(w.size);
            }
            else {
                    print(w.text);
            }
        }

        private void CreateImageTarget(string targetName, string targetPath)
        {
            GameObject imageTarget = new GameObject(targetName);
            var controller = imageTarget.AddComponent<ImageTargetController>();
            controller.SourceType = ImageTargetController.DataSource.ImageFile;
            controller.ImageFileSource.PathType = PathType.Absolute;
            controller.ImageFileSource.Path = targetPath;
            controller.ImageFileSource.Name = targetName;
            controller.Tracker = Filter;
            imageTargetDic.Add(targetName, controller);
            var cube = Instantiate(Cube);
            cube.transform.parent = imageTarget.transform;

            //make www
            var www = new WWW("http://192.168.4.171:5000/file");
            while (!www.isDone)
                System.Threading.Thread.Sleep(1);
            
            //create stream and load
            var textStream = new MemoryStream(Encoding.UTF8.GetBytes(www.text));
            var loadedObj = new OBJLoader().Load(textStream);
            loadedObj.transform.parent = imageTarget.transform;
            // Debug.Log(imageTarget.transform.GetChild);
            
            loadedObj.transform.position = new Vector3(0.5f,-0.5f,0f);
            loadedObj.transform.Rotate(-90,0,0);

            foreach (Transform child in loadedObj.transform)
            {
            
                if(child.name.Contains("window")){
                    child.GetComponent<Renderer>().GetComponent<Renderer>().material = mat;
                }
                else if(child.name.Contains ("Curve.001")){
                    child.GetComponent<Renderer>().GetComponent<Renderer>().material = plane;
                }
                else{
                    child.GetComponent<Renderer>().GetComponent<Renderer>().material = white;
                }
                
            }

        
        }

        public void StartCreateTarget()
        {
            StartCoroutine(TakePhotoCreateTarget());
        }

        public void ClearAllTarget()
        {
            creating = false;

            foreach (var obj in imageTargetDic)
                Destroy(obj.Value.gameObject);
            imageTargetDic = new Dictionary<string, ImageTargetController>();

            Dictionary<string, string> imageFileDic = GetImagesWithDir(directory);
            foreach (var path in imageFileDic)
                File.Delete(path.Value);
        }
    }
}
