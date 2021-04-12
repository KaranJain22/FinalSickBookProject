package com.comp.sickbook.ui.home;

import android.app.AlertDialog;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.comp.sickbook.Background.Person;
import com.comp.sickbook.R;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;
import com.google.firebase.installations.FirebaseInstallations;

import java.util.ArrayList;

public class HomeFragment extends Fragment {


    String userID;
    Person person;
    private AlertDialog.Builder dialogBuilder;
    private AlertDialog dialog;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);



    }
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        FirebaseFirestore db = FirebaseFirestore.getInstance();
        View root = inflater.inflate(R.layout.fragment_home, container, false);

        TextView homeEmailText = root.findViewById(R.id.accountName);
        Button changeButton = root.findViewById(R.id.ChangeAccountButton);
        changeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dialogBuilder = new AlertDialog.Builder(getContext());
                final View changeAccountPopup = getLayoutInflater().inflate(R.layout.account_popup, null);

                dialogBuilder.setView(changeAccountPopup);
                dialog = dialogBuilder.create();
                dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));

                EditText emailText = changeAccountPopup.findViewById(R.id.email);
                EditText passwordText = changeAccountPopup.findViewById(R.id.password);
                Button signInButton = changeAccountPopup.findViewById(R.id.signInButton);
                signInButton.setOnClickListener(new View.OnClickListener(){
                    @Override
                    public void onClick(View v) {


                        person.setEmail(emailText.getText().toString());
                        person.setPassword(passwordText.getText().toString());
                        db.collection("people").document(userID).set(person);
                        homeEmailText.setText(person.getEmail());
                        dialog.dismiss();


                    }

                });



                dialog.show();

            }
        });

        ImageView logo = root.findViewById(R.id.viewLogo);
        logo.setBackground(Drawable.createFromPath("file:///android_asset/logo.png"));



        FirebaseInstallations.getInstance().getId()        // attempt to get unique firebase user ID
                .addOnCompleteListener(new OnCompleteListener<String>() {
                    @Override
                    public void onComplete(@NonNull Task<String> task) {
                        if (task.isSuccessful()) {

                            userID = task.getResult();

                            DocumentReference personRef = db.collection("people").document(userID);
                            personRef.get().addOnSuccessListener(new OnSuccessListener<DocumentSnapshot>() {
                                @Override
                                public void onSuccess(DocumentSnapshot documentSnapshot) {
                                    if(!documentSnapshot.exists()){
                                        person = new Person();
                                        personRef.set(person);
                                    }
                                    else{
                                        person = documentSnapshot.toObject(Person.class);
                                    }

                                    if (person.getEmail()!=null)
                                        if(!person.getEmail().isEmpty())
                                            homeEmailText.setText(person.getEmail());





                                }
                            });



                        }

                    }


                });
























        return root;
    }
}