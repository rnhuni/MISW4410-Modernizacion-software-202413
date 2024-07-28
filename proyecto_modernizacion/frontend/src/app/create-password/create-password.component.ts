import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup, Validators } from "@angular/forms";

import { PasswordService } from './create.service';
import { IPassword } from '../models/password';

@Component({
  selector: 'app-create-password',
  templateUrl: './create-password.component.html',
  styleUrls: ['./create-password.component.css']
})
export class CreatePasswordComponent {
  public passwordForm!: FormGroup;

  constructor(private router: Router, 
    private createService: PasswordService,
    private toastr: ToastrService,
    private formBuilder: FormBuilder,) { }
  
  ngOnInit() {
    this.passwordForm = this.formBuilder.group({
      name: ["", [Validators.required, Validators.maxLength(50)]],
      password: ["", [Validators.required, Validators.maxLength(50)]],
      confirmPassword: ["", [Validators.required, Validators.maxLength(50)]],
      hint: ["", [Validators.required, Validators.maxLength(50)]],
    })
  }

  onCancel() {
    this.passwordForm.reset();
    this.router.navigate(['/passwords']);
  }

  public createPassword(password : IPassword): void{
    if (this.passwordForm.valid) {
      if (password.confirmPassword != password.password) {
        this.toastr.error("Error", "Las claves no coinciden")
        return
      }
      this.createService.createPassword(password).subscribe(
        passwordResult => {
          this.toastr.success("Confirmación", "Clave creada")
          this.passwordForm.reset();
          console.log("Creada con éxito")
          this.router.navigate(['/passwords']);
        }
      )
    }
  }
}
