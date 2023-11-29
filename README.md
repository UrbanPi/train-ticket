## ts-error-F21
### Original fault description
> **industrial fault description**:
> 
> Symptom：
> JAWS (a screen reader) misses reading some elements
> Root Cause：
> The “aria-labeled-by” element for accessibility cannot be located by the JAWS
> 
> **train_ticket replicated fault description**:
> 
> Just add the aria label in the login module.
> There are three input types to read —  Email, Password and Verification Code.
> When the cursor focuses on the input, the screen reader will read the value in it.
> Add the "aria-labelledby" label to the "Email" and "Password" inputs to first read the input name,
> so that user can make clear what the input value represent.
> But the "Verification Code" input doesn't add an "aria-labelledby" label
> So user will just heard the input's default value "abcd", it will confuse the user.
> 
> **fault replicate steps**:
> 
> setup system:
> 
> - Use docker-compose to setup the Train-Ticket System.
> - Install and start a screen reader software
> 
> fault reproduce manually step:
> 
> 1. Click [Flow one - Ticket Reserve]
> 2. Click [Tab] and focus the Email input, the screen reader will read the label and default value of this row
> 3. Continue click [Tab] until cursor focuses on the Verification Code row, 
> since it misses a "aria-labelledby" label, the screen reader will not read the "Verification Code" string. 
>  

### Notes
Email and password input fields have an `aria-labelelledby` attribute while the input for the verification code lacks one.
Behaviour with screen reader not tested.