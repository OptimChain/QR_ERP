/****** Object:  StoredProcedure [dbo].[Send_proc]    Script Date: 12/19/2020 3:59:04 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[Send_proc](
@Count int,
@ID int,
@add_true bit
)
AS
BEGIN 
SET NOCOUNT ON

	declare @_existing_quantity int = (select Qty from INVENTORY where [Inventory ID]=@ID)

	if(@_existing_quantity is not null)
	begin 
		if(@add_true=1)
			begin 
				update INVENTORY set Qty = @_existing_quantity-@Count where [Inventory ID]=@ID
			end
		if(@add_true=0)
			begin 
				update INVENTORY set Qty = @_existing_quantity+@Count where [Inventory ID]=@ID
			end
	end

END

