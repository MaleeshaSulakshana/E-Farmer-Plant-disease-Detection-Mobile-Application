package com.example.e_farmer;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;

public class DashboardActivity extends AppCompatActivity {

    private LinearLayout btnDetectLayout, btnDetailsLayout, btnSearchLayout, layoutDiseasesAndTreatments, layoutDetection,
                        btnImageCapture, btnUploadFromDevice, btnView, btnDetect;

    private ListView itemsList;

    private ImageView imageView;

    private static final int PICK_IMAGE = 100;
    private static final int CAMERA_PERM_CODE = 101;
    private static final int CAMERA_REQUEST_CODE = 102;
    private Uri imageUri = Uri.EMPTY;
    private String isCaptured = "no";

    private boolean doubleBackToExitPressedOnce = false;
    private Dialog exitDialog, detectionDialog, detailsDialog, loadingDialog;

    private ArrayList<DetailsItems> detailsArrayList = new ArrayList<>();

    private Bitmap bitmap = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

//        Get layouts
        exitDialog = new Dialog(DashboardActivity.this);
        exitDialog.setContentView(R.layout.exit_dialog_box);

        detectionDialog = new Dialog(DashboardActivity.this);
        detectionDialog.setContentView(R.layout.view_detection_details_dialog_box);

        detailsDialog = new Dialog(DashboardActivity.this);
        detailsDialog.setContentView(R.layout.view_details_dialog_box);

        loadingDialog = new Dialog(DashboardActivity.this);
        loadingDialog.setContentView(R.layout.waiting_dialog_box);

        imageView = (ImageView) this.findViewById(R.id.imageView);
        btnImageCapture = (LinearLayout) this.findViewById(R.id.btnImageCapture);
        btnUploadFromDevice = (LinearLayout) this.findViewById(R.id.btnUploadFromDevice);
        btnDetect = (LinearLayout) this.findViewById(R.id.btnDetect);

        btnDetectLayout = (LinearLayout) this.findViewById(R.id.btnDetectLayout);
        btnDetailsLayout = (LinearLayout) this.findViewById(R.id.btnDetailsLayout);
        layoutDiseasesAndTreatments = (LinearLayout) this.findViewById(R.id.layoutDiseasesAndTreatments);
        layoutDetection = (LinearLayout) this.findViewById(R.id.layoutDetection);

        itemsList = (ListView) this.findViewById(R.id.itemsList);


        layoutDetection.setVisibility(View.VISIBLE);
        layoutDiseasesAndTreatments.setVisibility(View.GONE);

        showDetailsItems();

        btnDetailsLayout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                layoutDetection.setVisibility(View.GONE);
                layoutDiseasesAndTreatments.setVisibility(View.VISIBLE);

                showDetailsItems();

            }
        });

        btnDetectLayout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                layoutDetection.setVisibility(View.VISIBLE);
                layoutDiseasesAndTreatments.setVisibility(View.GONE);

            }
        });

        itemsList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int i, long id) {

                getDiseaseAndTreatmentsDetails(detailsArrayList.get(i).getId());
            }
        });

        btnUploadFromDevice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                Open camera and capture image
                openGallery();
            }
        });

        btnImageCapture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

//                Get permission
                getPermission();
            }
        });

        btnDetect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                try {
                    detectDisease();
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        });

    }

    //    For open gallery
    private void openGallery()
    {
        Intent gallery = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        startActivityForResult(gallery, PICK_IMAGE);
    }

    //    For open camera
    private void openCamera()
    {
        Intent camera = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(camera, CAMERA_REQUEST_CODE);
    }


    //    Get permission
    private void getPermission()
    {

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[] {
                    Manifest.permission.CAMERA
            }, CAMERA_PERM_CODE);
        }
        else
        {
            openCamera();
        }

    }

    //    For get detection details
    private void showDetectionDetails(String plant, String disease)
    {
        Button btnExitYes, btnExitNo;
        TextView diseaseName, plantName;

        detectionDialog.show();

        btnExitYes = (Button) detectionDialog.findViewById(R.id.btnYes);
        diseaseName = (TextView) detectionDialog.findViewById(R.id.diseaseName);
        plantName = (TextView) detectionDialog.findViewById(R.id.plantName);

        plantName.setText(plant);
        diseaseName.setText(disease);

        btnExitYes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                layoutDetection.setVisibility(View.GONE);
                layoutDiseasesAndTreatments.setVisibility(View.VISIBLE);
                detectionDialog.dismiss();
            }
        });

        btnExitNo = (Button) detectionDialog.findViewById(R.id.btnNo);
        btnExitNo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                detectionDialog.dismiss();
            }
        });
    }

    private void getDiseaseAndTreatmentsDetails(int id)
    {
        ImageView btnClose, diseaseImage;
        TextView diseaseName, plantName, diseaseDetails, treatmentsDetails;
        detailsDialog.show();

        btnClose = (ImageView) detailsDialog.findViewById(R.id.btnClose);
        diseaseImage = (ImageView) detailsDialog.findViewById(R.id.diseaseImage);
        diseaseName = (TextView) detailsDialog.findViewById(R.id.diseaseName);
        plantName = (TextView) detailsDialog.findViewById(R.id.plantName);
        diseaseDetails = (TextView) detailsDialog.findViewById(R.id.diseaseDetails);
        treatmentsDetails = (TextView) detailsDialog.findViewById(R.id.treatmentsDetails);

        btnClose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                detailsDialog.dismiss();
            }
        });


        String URL = API.BASE_URL + "api/diseases_and_treatments/" + id;

        RequestQueue requestQueue = Volley.newRequestQueue(DashboardActivity.this);
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                URL,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        try {

                            if (response.length() > 0) {

                                JSONArray responseData = response.getJSONArray(0);

                                Integer id = (Integer) responseData.get(0);
                                String plant_name = (String) responseData.get(1);
                                String disease_name = (String) responseData.get(2);
                                String disease_details = (String) responseData.get(3);
                                String treatment_details = (String) responseData.get(4);
                                String image = API.ASSERT_URL + ((String) responseData.get(5));

                                plantName.setText(plant_name);
                                diseaseName.setText(disease_name);
                                diseaseDetails.setText(disease_details);
                                treatmentsDetails.setText(treatment_details);

                                Uri imgUri = Uri.parse(image);
                                Picasso.get().load(imgUri).into(diseaseImage);

                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(DashboardActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);


    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {

        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_PERM_CODE) {
            if (grantResults.length < 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                openCamera();
            } else {
                Toast.makeText(this, "Camera permission is required to use camera", Toast.LENGTH_SHORT).show();
            }
        }

    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){

        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && requestCode == PICK_IMAGE){
            imageUri = data.getData();
//            imageView.setImageURI(imageUri);
            try {
                bitmap = (Bitmap) MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
                imageView.setImageBitmap(bitmap );
            } catch (IOException e) {
                e.printStackTrace();
            }
            isCaptured = "no";

        }
        else if (resultCode == RESULT_OK && requestCode == CAMERA_REQUEST_CODE){

            Bitmap image = (Bitmap) data.getExtras().get("data");
            bitmap = image;
            imageView.setImageBitmap(image);
            imageUri = Uri.EMPTY;
            isCaptured = "yes";

        }

    }

    public String getStringImage(Bitmap bmp) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
        byte[] imageBytes = byteArrayOutputStream.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;

    }

    private void detectDisease() throws JSONException {

        if (bitmap != null) {

            String URL = API.BASE_URL + "api/detect_disease";

            loadingDialog.show();
            loadingDialog.setCancelable(false);
            loadingDialog.setCanceledOnTouchOutside(false);

            String image = getStringImage(bitmap);
            HashMap<String,String> params =  new HashMap<>();
            params.put("image", image);
            JSONObject parameter =  new JSONObject(params);
            JsonObjectRequest jsonObject = new JsonObjectRequest(Request.Method.POST, URL, parameter, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {

                    try {

                        String plant = response.getString("plant");
                        String disease = response.getString("disease");
//                    String accuracy = response.getString("accuracy");

                        bitmap = null;

                        imageView.setImageBitmap(null);
                        imageView.setBackgroundResource(R.drawable.logo);

                        loadingDialog.dismiss();
                        showDetectionDetails(plant, disease);

                    } catch (JSONException e) {
                        loadingDialog.dismiss();
                        e.printStackTrace();
                    }

                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    loadingDialog.dismiss();
                    Toast.makeText(DashboardActivity.this, error.getMessage().toString(), Toast.LENGTH_SHORT).show();
                }
            });


            RequestQueue queue = Volley.newRequestQueue(this);
            queue.add(jsonObject);

        } else {
            Toast.makeText(DashboardActivity.this, "Capture or select image to detect.", Toast.LENGTH_SHORT).show();
        }

    }

    private void showDetailsItems()
    {
        detailsArrayList.clear();
        itemsList.setAdapter(null);

        DetailsAdapter addonAdapter = new DetailsAdapter(this, R.layout.row_item_details, detailsArrayList);
        itemsList.setAdapter(addonAdapter);

        String URL = API.BASE_URL + "api/diseases_and_treatments";

        RequestQueue requestQueue = Volley.newRequestQueue(DashboardActivity.this);
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                URL,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        try {

                            for (int index = 0; index < response.length(); index++) {

                                JSONArray responseData = response.getJSONArray(index);

                                Integer id = (Integer) responseData.get(0);
                                String plant = (String) responseData.get(1);
                                String disease = (String) responseData.get(2);
                                String image = API.ASSERT_URL + ((String) responseData.get(5));

                                detailsArrayList.add(new DetailsItems(id, disease, plant, image));

                            }

                            addonAdapter.notifyDataSetChanged();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(DashboardActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }


//    Tap to close app
    @Override
    public void onBackPressed() {
        if (doubleBackToExitPressedOnce) {
            super.onBackPressed();
            return;
        }

        Button btnExitYes, btnExitNo;
        exitDialog.show();

        btnExitYes = (Button) exitDialog.findViewById(R.id.btnYes);
        btnExitYes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finishAffinity();
                System.exit(0);
            }
        });

        btnExitNo = (Button) exitDialog.findViewById(R.id.btnNo);
        btnExitNo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                exitDialog.dismiss();
            }
        });

    }

}

class DetailsItems {

    int id;
    String disease, plant, image;

    public DetailsItems(int id, String disease, String plant, String image) {
        this.id = id;
        this.disease = disease;
        this.plant = plant;
        this.image = image;
    }

    public int getId() {
        return id;
    }

    public String getDisease() {
        return disease;
    }

    public String getPlant() {
        return plant;
    }

    public String getImage() {
        return image;
    }
}

class DetailsAdapter extends ArrayAdapter<DetailsItems> {

    private Context mContext;
    private int mResource;

    public DetailsAdapter(@NonNull Context context, int resource, @NonNull ArrayList<DetailsItems> objects) {
        super(context, resource, objects);

        this.mContext = context;
        this.mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);
        convertView = layoutInflater.inflate(mResource, parent, false);

        TextView disease = (TextView) convertView.findViewById(R.id.disease);
        TextView plant = (TextView) convertView.findViewById(R.id.plant);
        ImageView image = (ImageView) convertView.findViewById(R.id.image);

        plant.setText(getItem(position).getPlant());
        disease.setText(getItem(position).getDisease());

        Uri imgUri = Uri.parse(getItem(position).getImage());
        Picasso.get().load(imgUri).into(image);

        return convertView;
    }

}